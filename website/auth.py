from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import BarangayUser, Farmer
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

### BARANGAY LOGIN (first step) ###
@auth.route('/login/barangay', methods=['GET', 'POST'])
def login_barangay():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = BarangayUser.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Barangay login successful!', category='success')
            return redirect(url_for('auth.login_farmer'))  # Go to farmer login
        else:
            flash('Invalid email or password.', category='error')

    return render_template("login_barangay.html", user=current_user)


### FARMER LOGIN (after barangay login) ###
@auth.route('/login/farmer', methods=['GET', 'POST'])
@login_required  # must be logged in as barangay
def login_farmer():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        farmer = Farmer.query.filter_by(username=username).first()

        if farmer and check_password_hash(farmer.password, password):
            # Store farmer session info
            session['farmer_id'] = farmer.id
            session['farmer_name'] = farmer.full_name
            flash(f"Welcome, {farmer.full_name}!", category='success')
            return redirect(url_for('views.farmer_dashboard'))  # change to your actual route
        else:
            flash('Invalid username or password.', category='error')

    return render_template("login_farmer.html")


### LOGOUT (clears everything) ###
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Also clear farmer session
    flash("Logged out successfully.", category="success")
    return redirect(url_for('auth.login_barangay'))
