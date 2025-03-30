from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from mlmodels.drying_time_model.predict_drying_time import predict_drying_time
from mlmodels.moisture_model.predict_moisture import predict_moisture
from .models import DryingRecord
from . import db
from datetime import datetime, date, timedelta
import serial, traceback, time
from dateutil.relativedelta import relativedelta


views = Blueprint('views', __name__)

def read_arduino_serial():
    try:
        with serial.Serial('COM4', 115200, timeout=2) as ser:
            time.sleep(2)
            ser.reset_input_buffer()
            ser.write(b'read\n')
            print("Sent 'read' to Arduino. Waiting for response...")
            line = ser.readline().decode().strip()
            print("Arduino says:", line)
            parts = line.split(",")
            if len(parts) == 3:
                return float(parts[0]), float(parts[1]), float(parts[2])
    except Exception as e:
        print("Error reading from Arduino:", e)
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
        # Compute shelf life as future date
        if final_moisture == 14:
            shelf_life = date_dried + timedelta(weeks=3)
        elif final_moisture == 12:
            shelf_life = date_dried + relativedelta(months=12)
        else:
            shelf_life = date_dried + relativedelta(years=1, months=3)

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
                               shelf_life=shelf_life,
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
            batch_name=data.get('batch_name'),
            initial_weight=float(data.get('initial_weight')),
            temperature=float(data.get('temperature')),
            humidity=float(data.get('humidity')),
            sensor_value=float(data.get('sensor_value')),
            initial_moisture=float(data.get('moisture_content')),
            final_moisture=float(data.get('final_moisture')),
            drying_time=data.get('drying_time'),
            final_weight=float(data.get('final_weight')),
            shelf_life=data.get('shelf_life'),
            date_planted=datetime.strptime(data.get('date_planted'), "%Y-%m-%d").date(),
            date_harvested=datetime.strptime(data.get('date_harvested'), "%Y-%m-%d").date(),
            date_dried=datetime.strptime(data.get('date_dried'), "%Y-%m-%d").date(),
            user_id=current_user.id
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
    user_records = DryingRecord.query.filter_by(user_id=current_user.id).order_by(DryingRecord.timestamp.desc()).all()
    return render_template("records.html", user=current_user, records=user_records)