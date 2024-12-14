from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# User Model
class User(db.Model):
    __tablename__ = 'users'  # Table name for the 'users' model

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Ensure this field exists
    bookings = db.relationship('Booking', backref='user', lazy=True)  # Relationship with Booking

    def __init__(self, username, email, password_hash, is_admin=False):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin  # Ensure this line is in the constructor


    def check_password(self, password):
        """Check if the given password matches the stored password hash."""
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        """Set the password hash for a given plain-text password."""
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}, {self.email}>'

# ParkingArea Model
class ParkingArea(db.Model):
    __tablename__ = 'parking_areas'  # Table name for the 'parking_areas' model

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', backref='parking_area', lazy=True)  # Relationship with Booking

    def __init__(self, name, location, available_slots):
        self.name = name
        self.location = location
        self.available_slots = available_slots

    def __repr__(self):
        return f'<ParkingArea {self.name}, Location: {self.location}>'

# Booking Model
class Booking(db.Model):
    __tablename__ = 'bookings'  # Table name for the 'bookings' model

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_area_id = db.Column(db.Integer, db.ForeignKey('parking_areas.id'), nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, parking_area_id, booking_time=None):
        self.user_id = user_id
        self.parking_area_id = parking_area_id
        if booking_time:
            self.booking_time = booking_time

    def __repr__(self):
        return f'<Booking {self.id}, User: {self.user_id}, Parking Area: {self.parking_area_id}>'
