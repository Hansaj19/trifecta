from flask import Flask
from .models import db  # Import your database model
from .views import views  # Import your views blueprint
from .auth import auth  # Import your auth blueprint (if you have one)


def create_app():
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Set your database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save resources

    # Initialize the database
    db.init_app(app)

    

    # Register the Blueprints
    app.register_blueprint(views, url_prefix='/')  # Blueprint for the main views
    app.register_blueprint(auth, url_prefix='/auth')  # Blueprint for authentication

    return app
