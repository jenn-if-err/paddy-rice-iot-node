from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

### BARANGAY USER (for logging into the device) ###
class BarangayUser(db.Model, UserMixin):
    __tablename__ = 'barangay_users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email-based login
    password = db.Column(db.String(150), nullable=False)
    barangay_name = db.Column(db.String(150), nullable=False)

    farmers = db.relationship('Farmer', backref='barangay_user', lazy=True)

### FARMER (individual user who logs in after barangay login) ###
class Farmer(db.Model):
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    barangay_id = db.Column(db.Integer, db.ForeignKey('barangay_users.id'), nullable=False)

    records = db.relationship('DryingRecord', backref='farmer', lazy=True)

### DRYING RECORD (linked to Farmer) ###
class DryingRecord(db.Model):
    __tablename__ = 'drying_records'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    batch_name = db.Column(db.String(150), nullable=False)

    # Sensor and drying input values
    initial_weight = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    sensor_value = db.Column(db.Float, nullable=False)
    initial_moisture = db.Column(db.Float, nullable=False)
    final_moisture = db.Column(db.Float, nullable=False)

    # Prediction results
    drying_time = db.Column(db.String(10), nullable=False)
    final_weight = db.Column(db.Float, nullable=False)
    shelf_life = db.Column(db.String(50), nullable=False)

    # Foreign key: linked to Farmer
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)

    # Crop cycle dates
    date_planted = db.Column(db.Date)
    date_harvested = db.Column(db.Date)
    date_dried = db.Column(db.Date)
