from app import db
from app.models import User
from app.utils import generate_password_hash
from app import create_app

# Initialize the app and database
app = create_app()

# Set the admin email, password, and other details
admin_email = 'waqarsoftware310@gmail.com'  # This should match the ADMIN_EMAIL from .env
admin_password = 'brock123'  # The admin password you want to set
admin_name = 'Admin User'  # Admin user's name

# Create the admin user in the database
with app.app_context():
    # Check if the admin user already exists
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        # Hash the password before storing it
        hashed_password = generate_password_hash(admin_password)
        
        # Create a new admin user
        new_admin_user = User(
            username=admin_name, 
            email=admin_email, 
            password_hash=hashed_password,
            is_admin=True  # Set the is_admin flag to True
        )
        
        # Add the new user to the database
        db.session.add(new_admin_user)
        db.session.commit()

        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
