from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__,template_folder='../templates',static_folder='../static')

    # App configuration
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # Initialize database
    db.init_app(app)

    from .models import User 
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register Blueprints (modular routes)
    from .routes import main
    app.register_blueprint(main)

    return app
