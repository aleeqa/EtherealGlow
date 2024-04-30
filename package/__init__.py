from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize SQLAlchemy and Bcrypt extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

# Define the name of the database file
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"  # Set a secret key for the application
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Set the URI for the SQLite database
   
    # Initialize extensions with the Flask application
    db.init_app(app)
    bcrypt.init_app(app)

    # Importing blueprints
    from main import main_blueprint

    # Import models to ensure they are registered with SQLAlchemy
    from .models import User

    # Create the database if it doesn't exist
    create_database(app)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "main.login"  # Specify the login view route
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Register blueprints with the application
    app.register_blueprint(main_blueprint)

    return app

def create_database(app):
    # Check if the database file exists, if not, create it
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()  # Create all tables defined in the SQLAlchemy models
            print("Created database!")


