from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .api import authenticate_user, fetch_farmer_data, fetch_user_data, fetch_barangay_data, fetch_municipality_data
from .models import Farmer, Barangay, Municipality, User
import requests
auth = Blueprint('auth', __name__)
from flask import session



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        password = request.form.get('password')

        # Try to authenticate as a local farmer
        farmer = Farmer.query.filter_by(username=username_or_email).first()
        if farmer and check_password_hash(farmer.password, password):
            session.permanent = True
            session['password'] = password  # ✅ Store password for syncing
            login_user(farmer, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))

        # Try remote authentication
        REMOTE_URL = "https://paddy-rice-tracker.onrender.com"
        LOGIN_ENDPOINT = f"{REMOTE_URL}/login"

        try:
            login_resp = requests.post(
                LOGIN_ENDPOINT,
                data={"email": username_or_email, "password": password},
                headers={"Accept": "application/json"}
            )

            if login_resp.status_code == 200:
                session.permanent = True
                session['password'] = password
                print("Password stored in session:", session.get('password'))

                from .api import fetch_user_data, fetch_farmer_data, fetch_barangay_data, fetch_municipality_data

                all_users = fetch_user_data()
                if all_users:
                    for u in all_users:
                        existing_user = User.query.filter_by(email=u['email']).first()
                        if not existing_user:
                            db.session.add(User(
                                id=u['id'],
                                email=u['email'],
                                full_name=u['full_name'],
                                role=u['role'],
                                password="not_used",
                                barangay_id=u['barangay_id'],
                                municipality_id=u['municipality_id']
                            ))

                barangays = fetch_barangay_data()
                if barangays:
                    for b in barangays:
                        existing = Barangay.query.filter_by(id=b['id']).first()
                        if existing:
                            existing.name = b['name']
                            existing.municipality_id = b['municipality_id']
                        else:
                            db.session.add(Barangay(
                                id=b['id'],
                                name=b['name'],
                                municipality_id=b['municipality_id']
                            ))

                municipalities = fetch_municipality_data()
                if municipalities:
                    for m in municipalities:
                        existing = Municipality.query.filter_by(id=m['id']).first()
                        if existing:
                            existing.name = m['name']
                        else:
                            db.session.add(Municipality(
                                id=m['id'],
                                name=m['name']
                            ))

                farmer_data = fetch_farmer_data(username_or_email)
                if farmer_data:
                    existing_farmer = Farmer.query.filter_by(username=farmer_data['username']).first()
                    if not existing_farmer:
                        db.session.add(Farmer(
                            uuid=farmer_data['uuid'],
                            username=farmer_data['username'],
                            password=generate_password_hash(password),
                            first_name=farmer_data['first_name'],
                            middle_name=farmer_data.get('middle_name'),
                            last_name=farmer_data['last_name'],
                            barangay_id=farmer_data['barangay_id']
                        ))
                db.session.commit()

                farmer = Farmer.query.filter_by(username=username_or_email).first()
                if farmer:
                    login_user(farmer, remember=True)
                    flash("Logged in successfully!", "success")
                    return redirect(url_for("views.home"))
                else:
                    flash("Farmer created but login failed.", "error")

        except requests.ConnectionError:
            flash("No internet connection. Please try again later.", "error")

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
        # authenticate and fetch data
        if authenticate_user(current_user.username, session.get('password')):
            farmer_data = fetch_farmer_data(current_user.username)

            # store farmer data
            if farmer_data:
                farmer = Farmer.query.filter_by(username=farmer_data['username']).first()
                if farmer:
                    # update existing farmer
                    farmer.first_name = farmer_data['first_name']
                    farmer.middle_name = farmer_data.get('middle_name')
                    farmer.last_name = farmer_data['last_name']
                    farmer.barangay_id = farmer_data['barangay_id']
                else:
                    # create new farmer
                    new_farmer = Farmer(
                        username=farmer_data['username'],
                        password=generate_password_hash(session.get('password'), method='pbkdf2:sha256'),
                        first_name=farmer_data['first_name'],
                        middle_name=farmer_data.get('middle_name'),
                        last_name=farmer_data['last_name'],
                        barangay_id=farmer_data['barangay_id']
                    )
                    db.session.add(new_farmer)
                    db.session.commit()  

            # store barangay and municipality data
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
                        db.session.commit()  

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

            db.session.commit()
            flash('Data synced successfully!', category='success')
        else:
            flash('Authentication failed. Please log in again.', category='error')
    except Exception as e:
        flash(f"Sync failed: {str(e)}", category='error')

    return redirect(url_for('auth.login'))