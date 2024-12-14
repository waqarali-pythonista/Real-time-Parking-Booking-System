# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager
# from flask_mail import Mail
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os

# # Initialize the extensions
# db = SQLAlchemy()
# migrate = Migrate()
# jwt = JWTManager()
# mail = Mail()
# cors = CORS()

# # Load environment variables from .env file
# load_dotenv()

# def create_app():
#     """
#     Factory function to create and initialize the Flask application.
#     Sets up configurations, extensions, and routes.
#     """
#     app = Flask(__name__)

#     # Load configurations from the Config class
#     app.config.from_object('app.config.Config')

#     # Initialize extensions with the Flask app instance
#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
#     mail.init_app(app)
#     cors.init_app(app, origins=app.config['CORS_ORIGINS'])  # Set up CORS based on config

#     # Register blueprints (routes)
#     from app.routes import main  # Import the main blueprint from routes.py
#     app.register_blueprint(main)  # Register the blueprint

#     return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cors = CORS()

# Load environment variables from .env file
load_dotenv()

def create_app():
    """
    Factory function to create and initialize the Flask application.
    Sets up configurations, extensions, and routes.
    """
    app = Flask(__name__)
    CORS(app)

    # Load configurations from the Config class
    app.config.from_object('app.config.Config')

    # Initialize extensions with the Flask app instance
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])  # Set up CORS based on config

    # Register blueprints (routes)
    from app.admin import admin  # Import admin blueprint inside create_app function to avoid circular imports
    app.register_blueprint(admin)  # Register the blueprint for admin routes

    # Import main routes and register them after app initialization
    from app.routes import main  # Import the main blueprint
    app.register_blueprint(main)  # Register the main blueprint

    return app
