import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Secret keys for securing the app and JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'de208c474fb0d851fbc07cba2af9e8c89e5aeb22649301db')  # Default to your provided secret key
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '55ac2169b44f2c69c66f9a9a3760abee6c6c6a4dfe241057bf6329c009f8ee35')  # Default to your provided JWT secret key
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///parking_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
    
    # Email configuration for Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
    MAIL_PORT = 587  # Gmail SMTP port
    MAIL_USE_TLS = True  # Use TLS for secure email sending
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Email used to send emails (from your .env)
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Password for the sender email (from your .env)
    ADMIN_EMAIL = 'waqarsoftware310@gmail.com'  # Hardcoded admin email as requested
    
    # Ensure MAIL_DEBUG is treated as a boolean
    MAIL_DEBUG = os.getenv('MAIL_DEBUG', 'False').lower() in ['true', '1', 't', 'y', 'yes']

    # CORS (Cross-Origin Resource Sharing) settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')  # Allow requests from all domains or specify allowed domains

    # Configure session settings for Flask if needed
    SESSION_COOKIE_SECURE = True  # Set cookies to be secure over HTTPS
    SESSION_PERMANENT = False  # Session will not be permanent by default
    PERMANENT_SESSION_LIFETIME = 3600  # Session lifetime (seconds)

    # JWT Token Expiry Time (default: 1 hour)
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour expiration for JWT tokens
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 24 hours expiration for refresh tokens

    # Logging configuration (optional, useful for debugging in production)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')  # Set logging level
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')  # Log output file

    # Flask application config settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')  # Set environment (development, production, testing)

    # Other custom configurations
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file upload size (16 MB)

    # Configure allowed file types for upload if needed (optional)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

    # Other custom settings can go here
    DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Whether to enable debugging mode, use 'True'/'False'
