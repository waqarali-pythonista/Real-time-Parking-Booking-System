import os
from werkzeug.security import generate_password_hash
import random
import string

# Function to hash passwords
def hash_password(password):
    """
    Utility function to hash the password before saving it to the database.
    """
    return generate_password_hash(password)

# Function to generate a random booking ID
def generate_booking_id():
    """
    Utility function to generate a random booking ID (alphanumeric).
    The length of the booking ID can be adjusted.
    """
    characters = string.ascii_letters + string.digits
    booking_id = ''.join(random.choice(characters) for i in range(10))
    return booking_id

# Function to check parking availability
def is_parking_available(parking_slot):
    """
    Utility function to check if a parking slot is available.
    Returns True if available, False otherwise.
    """
    return parking_slot.is_available

# Function to create JWT token with expiry
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

def create_jwt_token(user_id, expiration_time=1):
    """
    Utility function to create a JWT token.
    Default expiration time is set to 1 hour, but it can be adjusted.
    """
    expiration = timedelta(hours=expiration_time)
    access_token = create_access_token(identity=user_id, expires_delta=expiration)
    return access_token

# Function to send email confirmation (as utility to avoid redundancy)
from app.email import send_confirmation_email

def send_booking_confirmation(user_email, parking_slot):
    """
    Utility function to send the booking confirmation email to the user.
    Calls the send_confirmation_email method from email.py.
    """
    send_confirmation_email(user_email, parking_slot)

# Utility function to calculate available slots in a parking area
def get_available_slots(parking_area):
    """
    Utility function to calculate available parking slots in a given parking area.
    Returns the count of available slots.
    """
    available_slots = [slot for slot in parking_area.parking_slots if slot.is_available]
    return len(available_slots)

# Utility function to generate a random slot number
def generate_random_slot_number():
    """
    Utility function to generate a random parking slot number (for example, 101, 102, 103, etc.)
    This can be useful when creating new slots for a parking area.
    """
    return random.randint(1, 500)  # You can set the range according to your needs
