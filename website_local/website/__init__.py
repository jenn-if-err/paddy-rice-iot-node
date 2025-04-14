from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta  

# Initialize SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) 

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth
    from .api import api
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    # Import models
    from .models import Farmer, DryingRecord, Municipality, Barangay, User
    create_database(app)

    # Flask-Login Setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id_str):
        from .models import Farmer
        try:
            if user_id_str.startswith('farmer-'):
                user_id = user_id_str.split('-')[1]
                return Farmer.query.get(int(user_id))
        except (ValueError, AttributeError):
            return None

    return app

def create_database(app):
    db_path = path.join('website', DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("Created new SQLite database at:", db_path)
