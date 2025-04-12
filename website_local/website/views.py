from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from mlmodels.drying_time_model.predict_drying_time import predict_drying_time
from mlmodels.moisture_model.predict_moisture import predict_moisture
from .models import DryingRecord, Farmer, Municipality, Barangay
from . import db
from datetime import datetime, date, timedelta
import serial, traceback, time, platform, os, requests
from dateutil.relativedelta import relativedelta
from .api import authenticate_user, fetch_farmer_data, fetch_related_data
import uuid

PASSWORD = os.environ.get("REMOTE_PASSWORD")
views = Blueprint('views', __name__)


def read_arduino_serial():
    try:
        # detect OS and choose port
        if platform.system() == 'Windows':
            port = 'COM4'
        else:
            port = '/dev/ttyUSB0'  # or '/dev/ttyACM0' 

        # Check if the port is available
        if not os.path.exists(port):
            print("Arduino not found. Using default values.")
            return 20.0, 25.0, 60.0  # Default sensor_value, temperature, humidity

        with serial.Serial(port, 115200, timeout=2) as ser:
            time.sleep(2)
            ser.reset_input_buffer()
            ser.write(b'read\n')
            print("Sent 'read' to Arduino. Waiting for response...")
            line = ser.readline().decode().strip()
            print("Arduino says:", line)

            parts = line.split(",")
            if len(parts) == 3:
                return float(parts[0]), float(parts[1]), float(parts[2])
            else:
                print("Invalid response format from Arduino.")
    except Exception as e:
        print("Error reading from Arduino:", e)
        print("Using default values.")
        return 20.0, 25.0, 60.0  # Default sensor_value, temperature, humidity

    return None, None, None


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        try:
            initial_weight = float(request.form.get('initial_weight'))
            final_moisture = float(request.form.get('final_moisture'))
            date_planted = datetime.strptime(request.form.get('date_planted'), "%Y-%m-%d").date()
            date_harvested = datetime.strptime(request.form.get('date_harvested'), "%Y-%m-%d").date()
            batch_name = request.form.get('batch_name')
            date_dried = date.today()

            sensor_value, temperature, humidity = read_arduino_serial()
            if None in (sensor_value, temperature, humidity):
                flash("Error: could not read sensor data from Arduino.", category="error")
                return redirect(url_for('views.home'))

            moisture_content = round(predict_moisture(sensor_value, temperature, humidity), 2)

            return render_template("readings.html", user=current_user,
                                   batch_name=batch_name,
                                   initial_weight=initial_weight,
                                   final_moisture=final_moisture,
                                   sensor_value=sensor_value,
                                   temperature=temperature,
                                   humidity=humidity,
                                   moisture_content=moisture_content,
                                   date_planted=date_planted,
                                   date_harvested=date_harvested,
                                   date_dried=date_dried)
        except Exception as e:
            traceback.print_exc()
            flash(f"Error processing form: {e}", category="error")

    return render_template("home.html", user=current_user)

@views.route('/calculate', methods=['POST'])
@login_required
def calculate():
    try:
        data = request.form
        initial_weight = float(data.get('initial_weight'))
        temperature = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
        sensor_value = float(data.get('sensor_value'))
        moisture_content = float(data.get('moisture_content'))
        final_moisture = float(data.get('final_moisture'))
        batch_name = data.get('batch_name')

        date_planted = request.form.get('date_planted')
        date_harvested = request.form.get('date_harvested')

        if not date_planted or not date_harvested:
            flash("Missing date values. Please make sure all fields are filled.", category="error")
            return redirect(url_for('views.home'))

        date_planted = datetime.strptime(date_planted, "%Y-%m-%d").date()
        date_harvested = datetime.strptime(date_harvested, "%Y-%m-%d").date()


        hours, minutes = predict_drying_time(moisture_content, temperature, humidity, final_moisture)
        drying_time = f"{hours}:{minutes:02d}"

        final_weight = round(initial_weight * ((1 - moisture_content / 100) / (1 - final_moisture / 100)), 2)

        date_dried = date.today()

        if final_moisture == 14:
            due_date = date_dried + timedelta(weeks=3)
        elif final_moisture == 12:
            due_date = date_dried + relativedelta(months=12)
        else:
            due_date = date_dried + relativedelta(years=1, months=3)

        return render_template("prediction.html", user=current_user,
                               batch_name=batch_name,
                               initial_weight=initial_weight,
                               temperature=temperature,
                               humidity=humidity,
                               sensor_value=sensor_value,
                               moisture_content=moisture_content,
                               final_moisture=final_moisture,
                               drying_time=drying_time,
                               final_weight=final_weight,
                               due_date=due_date,
                               date_planted=date_planted,
                               date_harvested=date_harvested,
                               date_dried=date_dried)

    except Exception as e:
        traceback.print_exc()
        flash(f"Calculation error: {e}", category="error")
        return redirect(url_for('views.home'))

@views.route('/save', methods=['POST'])
@login_required
def save_prediction():
    try:
        data = request.form

        new_record = DryingRecord(
            uuid=str(uuid.uuid4()),  # ✅ unique for syncing
            batch_name=data.get('batch_name'),
            initial_weight=float(data.get('initial_weight')),
            temperature=float(data.get('temperature')),
            humidity=float(data.get('humidity')),
            sensor_value=float(data.get('sensor_value')),
            initial_moisture=float(data.get('moisture_content')),
            final_moisture=float(data.get('final_moisture')),
            drying_time=data.get('drying_time'),
            final_weight=float(data.get('final_weight')),

            due_date=datetime.strptime(data.get('due_date'), "%Y-%m-%d").date(),
            date_planted=datetime.strptime(data.get('date_planted'), "%Y-%m-%d").date(),
            date_harvested=datetime.strptime(data.get('date_harvested'), "%Y-%m-%d").date(),
            date_dried=datetime.strptime(data.get('date_dried'), "%Y-%m-%d").date(),

            synced=False,  # ✅ not yet uploaded
            synced_at=None,  # ✅ will be filled during sync

            farmer_id=current_user.id,
            barangay_id=getattr(current_user, 'barangay_id', None),  # ✅ if available
            municipality_id=getattr(current_user, 'municipality_id', None),  # optional
            farmer_name=getattr(current_user, 'full_name', None)  # optional
        )

        db.session.add(new_record)
        db.session.commit()
        flash("Prediction saved successfully!", category="success")
        return redirect(url_for('views.records'))

    except Exception as e:
        traceback.print_exc()
        flash(f"Error saving prediction: {e}", category="error")
        return redirect(url_for('views.home'))

@views.route('/records')
@login_required
def records():
    user_records = DryingRecord.query.filter_by(farmer_id=current_user.id).order_by(DryingRecord.timestamp.desc()).all()
    return render_template("records.html", user=current_user, records=user_records)

@views.route('/sync-to-remote', methods=['GET', 'POST'])
@login_required
def sync_to_remote():
    REMOTE_URL = "http://localhost:5001"
    LOGIN_ENDPOINT = f"{REMOTE_URL}/login"
    SYNC_ENDPOINT = f"{REMOTE_URL}/api/sync"
    FETCH_ENDPOINT = f"{REMOTE_URL}/api/fetch"

    EMAIL = current_user.email
    PASSWORD = session.get("password")  # Get password from session (no re-login required)

    if not PASSWORD:
        flash("Please log in again to sync.", "danger")
        return redirect(url_for("auth.login"))

    session_requests = requests.Session()

    # Log in remotely (using the session's password)
    login_resp = session_requests.post(LOGIN_ENDPOINT, data={"email": EMAIL, "password": PASSWORD})

    if "Logged in successfully!" not in login_resp.text:
        flash("Remote login failed. Check your credentials.", "danger")
        return redirect(url_for("views.home"))

    # Upload unsynced records
    unsynced_records = DryingRecord.query.filter_by(farmer_id=current_user.id, synced=False).all()

    if unsynced_records:
        payload = {"records": [
            {
                "uuid": r.uuid,
                "batch_name": r.batch_name,
                "initial_weight": r.initial_weight,
                "temperature": r.temperature,
                "humidity": r.humidity,
                "sensor_value": r.sensor_value,
                "initial_moisture": r.initial_moisture,
                "final_moisture": r.final_moisture,
                "drying_time": r.drying_time,
                "final_weight": r.final_weight,
                "date_planted": r.date_planted,
                "date_harvested": r.date_harvested,
                "due_date": r.due_date,
                "farmer_id": r.farmer_id,
            } for r in unsynced_records
        ]}

        sync_resp = session_requests.post(SYNC_ENDPOINT, json=payload)

        if sync_resp.status_code == 200:
            for r in unsynced_records:
                r.synced = True
            db.session.commit()
            flash(f"Successfully synced {len(unsynced_records)} records.", "success")
        else:
            flash(f"Sync failed: {sync_resp.text}", "danger")
            return redirect(url_for("views.home"))

    # Fetch new data
    fetch_resp = session_requests.get(FETCH_ENDPOINT)

    if fetch_resp.status_code == 200:
        new_data = fetch_resp.json()
        for record in new_data:
            existing_record = DryingRecord.query.filter_by(uuid=record['uuid']).first()
            if existing_record:
                # Convert date strings to date objects
                date_planted_str = record.get('date_planted')
                date_harvested_str = record.get('date_harvested')
                due_date_str = record.get('due_date')

                try:
                    existing_record.initial_weight = record['initial_weight']
                    existing_record.temperature = record['temperature']
                    existing_record.humidity = record['humidity']
                    existing_record.sensor_value = record['sensor_value']
                    existing_record.initial_moisture = record['initial_moisture']
                    existing_record.final_moisture = record['final_moisture']
                    existing_record.drying_time = record['drying_time']
                    existing_record.final_weight = record['final_weight']
                    existing_record.date_planted = datetime.strptime(date_planted_str, '%Y-%m-%d').date() if date_planted_str else None
                    existing_record.date_harvested = datetime.strptime(date_harvested_str, '%Y-%m-%d').date() if date_harvested_str else None
                    existing_record.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
                except ValueError as e:
                    print(f"Date conversion error: {e}")
                    # You might want to skip this record or set a default date
            else:
                # Convert date strings to date objects
                date_planted_str = record.get('date_planted')
                date_harvested_str = record.get('date_harvested')
                due_date_str = record.get('due_date')

                try:
                    date_planted = datetime.strptime(date_planted_str, '%Y-%m-%d').date() if date_planted_str else None
                    date_harvested = datetime.strptime(date_harvested_str, '%Y-%m-%d').date() if date_harvested_str else None
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
                except ValueError as e:
                    print(f"Date conversion error: {e}")
                    # You might want to skip this record or set a default date

                # Create a new DryingRecord
                new_record = DryingRecord(
                    uuid=record['uuid'],
                    initial_weight=record['initial_weight'],
                    temperature=record['temperature'],
                    humidity=record['humidity'],
                    sensor_value=record['sensor_value'],
                    initial_moisture=record['initial_moisture'],
                    final_moisture=record['final_moisture'],
                    drying_time=record['drying_time'],
                    final_weight=record['final_weight'],
                    date_planted=date_planted,
                    date_harvested=date_harvested,
                    due_date=due_date,
                    farmer_id=current_user.id
                )
                db.session.add(new_record)
        db.session.commit()
        flash("Data fetched and merged successfully!", "success")
    else:
        flash(f"Failed to fetch data: {fetch_resp.text}", "danger")

    return redirect(url_for("views.home"))