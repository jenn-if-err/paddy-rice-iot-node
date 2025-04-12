from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .api import authenticate_user, fetch_farmer_data, fetch_related_data
from .models import Farmer, Barangay, Municipality
import requests
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        password = request.form.get('password')

        # Check if the farmer exists locally
        farmer = Farmer.query.filter_by(username=username_or_email).first()

        if farmer and check_password_hash(farmer.password, password):
            login_user(farmer, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            # Attempt to authenticate the user via the remote app
            REMOTE_URL = "http://localhost:5001"
            LOGIN_ENDPOINT = f"{REMOTE_URL}/login"

            try:
                login_resp = requests.post(
                    LOGIN_ENDPOINT,
                    data={"email": username_or_email, "password": password},
                    headers={"Accept": "application/json"}
                )

                if login_resp.status_code == 200:
                    # Store password in session to allow syncing records
                    session['password'] = password

                    # Query the remote database for farmer details
                    FARMER_ENDPOINT = f"{REMOTE_URL}/api/farmers/{username_or_email}"
                    farmer_resp = requests.get(FARMER_ENDPOINT, headers={"Accept": "application/json"})

                    if farmer_resp.status_code == 200:
                        farmer_data = farmer_resp.json()
                        # Create the farmer in the local database
                        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

                        new_farmer = Farmer(
                            username=farmer_data['username'],
                            password=hashed_password,
                            first_name=farmer_data['first_name'],
                            middle_name=farmer_data.get('middle_name'),
                            last_name=farmer_data['last_name'],
                            barangay_id=farmer_data['barangay_id']
                        )
                        db.session.add(new_farmer)

                        # Fetch and update barangay and municipality data
                        barangays, municipalities = fetch_related_data()

                        if barangays:
                            for barangay_data in barangays:
                                barangay = Barangay.query.filter_by(id=barangay_data['id']).first()
                                if barangay:
                                    barangay.name = barangay_data['name']
                                    barangay.municipality_id = barangay_data['municipality_id']
                                else:
                                    new_barangay = Barangay(
                                        id=barangay_data['id'],
                                        name=barangay_data['name'],
                                        municipality_id=barangay_data['municipality_id']
                                    )
                                    db.session.add(new_barangay)

                        if municipalities:
                            for municipality_data in municipalities:
                                municipality = Municipality.query.filter_by(id=municipality_data['id']).first()
                                if municipality:
                                    municipality.name = municipality_data['name']
                                else:
                                    new_municipality = Municipality(
                                        id=municipality_data['id'],
                                        name=municipality_data['name']
                                    )
                                    db.session.add(new_municipality)

                        db.session.commit()

                        # Log the new farmer in locally
                        login_user(new_farmer)
                        return redirect(url_for('views.home'))

            except requests.ConnectionError:
                flash('No internet connection. Please try again later.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sync', methods=['GET'])
@login_required
def sync():
    try:
        # Authenticate and fetch data
        if authenticate_user(current_user.username, session.get('password')):
            farmer_data = fetch_farmer_data(current_user.username)
            barangays, municipalities = fetch_related_data()

            # Store farmer data
            if farmer_data:
                farmer = Farmer.query.filter_by(username=farmer_data['username']).first()
                if farmer:
                    # Update existing farmer
                    farmer.first_name = farmer_data['first_name']
                    farmer.middle_name = farmer_data.get('middle_name')
                    farmer.last_name = farmer_data['last_name']
                    farmer.barangay_id = farmer_data['barangay_id']
                else:
                    # Create new farmer
                    new_farmer = Farmer(
                        username=farmer_data['username'],
                        password=generate_password_hash(session.get('password'), method='pbkdf2:sha256'),
                        first_name=farmer_data['first_name'],
                        middle_name=farmer_data.get('middle_name'),
                        last_name=farmer_data['last_name'],
                        barangay_id=farmer_data['barangay_id']
                    )
                    db.session.add(new_farmer)

            # Store barangay and municipality data
            if barangays:
                for barangay_data in barangays:
                    barangay = Barangay.query.filter_by(id=barangay_data['id']).first()
                    if barangay:
                        barangay.name = barangay_data['name']
                        barangay.municipality_id = barangay_data['municipality_id']
                    else:
                        new_barangay = Barangay(
                            id=barangay_data['id'],
                            name=barangay_data['name'],
                            municipality_id=barangay_data['municipality_id']
                        )
                        db.session.add(new_barangay)

            if municipalities:
                for municipality_data in municipalities:
                    municipality = Municipality.query.filter_by(id=municipality_data['id']).first()
                    if municipality:
                        municipality.name = municipality_data['name']
                    else:
                        new_municipality = Municipality(
                            id=municipality_data['id'],
                            name=municipality_data['name']
                        )
                        db.session.add(new_municipality)

            db.session.commit()
            flash('Data synced successfully!', category='success')
        else:
            flash('Authentication failed. Please log in again.', category='error')
    except Exception as e:
        flash(f"Sync failed: {str(e)}", category='error')

    return redirect(url_for('auth.login'))