from flask import Blueprint, request, jsonify
from app import db
from app.models import User, ParkingArea, Booking
from app.utils import generate_password_hash
from app.email import send_confirmation_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
main = Blueprint('main', __name__)

# Signup route
@main.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')  # Name is used as the username

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists"}), 400

    try:
        # Generate hashed password
        password_hash = generate_password_hash(password)

        # Create new user
        new_user = User(username=name, email=email, password_hash=password_hash)

        # Add to the database
        db.session.add(new_user)
        db.session.commit()

        # Send confirmation email (no parking_slot needed)
        send_confirmation_email(email)

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"message": "Error creating user", "error": str(e)}), 500

# Login route
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Check if user exists
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Create JWT token for the user
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Get user details (JWT protected)
@main.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    return jsonify({"message": "User not found"}), 404

# Route to view all parking areas
@main.route('/parking-areas', methods=['GET'])
def get_parking_areas():
    parking_areas = ParkingArea.query.all()
    result = []

    for area in parking_areas:
        result.append({
            "id": area.id,
            "name": area.name,
            "location": area.location,
            "available_slots": area.available_slots
        })

    return jsonify(result)

# Route to book a parking slot
@main.route('/book-parking', methods=['POST'])
@jwt_required()


def book_parking():
    # data = request.get_json()

    # parking_area_id = data.get('parking_area_id')
    # booking_time = data.get('booking_time')

    # # Check if parking area exists
    # parking_area = ParkingArea.query.get(parking_area_id)
    # if not parking_area:
    #     return jsonify({"message": "Parking area not found"}), 404

    # # Check availability of parking slot
    # if parking_area.available_slots <= 0:
    #     return jsonify({"message": "No available slots"}), 400

    # # Create the booking
    # booking = Booking(user_id=get_jwt_identity(), parking_area_id=parking_area.id, booking_time=booking_time)

    # try:
    #     db.session.add(booking)
    #     db.session.commit()

    #     # Update available slots for the parking area
    #     parking_area.available_slots -= 1
    #     db.session.commit()

    #     return jsonify({"message": "Booking successful"}), 201
    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({"message": "Error booking parking", "error": str(e)}), 500
    
    data = request.get_json()

    parking_area_id = data.get('parking_area_id')
    booking_time_str = data.get('booking_time')

    # Convert the booking_time from string to datetime
    try:
        booking_time = datetime.strptime(booking_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"message": "Invalid booking time format. Please use 'YYYY-MM-DD HH:MM:SS'."}), 400

    # Check if parking area exists
    parking_area = ParkingArea.query.get(parking_area_id)
    if not parking_area:
        return jsonify({"message": "Parking area not found"}), 404

    # Check availability of parking slot
    if parking_area.available_slots <= 0:
        return jsonify({"message": "No available slots"}), 400

    # Create the booking
    booking = Booking(
        user_id=get_jwt_identity(), 
        parking_area_id=parking_area.id, 
        booking_time=booking_time
    )

    try:
        db.session.add(booking)
        db.session.commit()

        # Update available slots for the parking area
        parking_area.available_slots -= 1
        db.session.commit()

        return jsonify({"message": "Booking successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error booking parking", "error": str(e)}), 500








# Route to cancel parking booking
@main.route('/cancel-booking/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    # Check if the current user is the owner of the booking
    if booking.user_id != get_jwt_identity():
        return jsonify({"message": "You are not authorized to cancel this booking"}), 403

    # Delete the booking and update the available slots for the parking area
    parking_area = ParkingArea.query.get(booking.parking_area_id)
    parking_area.available_slots += 1

    try:
        db.session.delete(booking)
        db.session.commit()

        # Update available slots
        db.session.commit()

        return jsonify({"message": "Booking cancelled successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error cancelling booking", "error": str(e)}), 500

# Admin route to view all parking areas
@main.route('/admin/parking-areas', methods=['GET'])
@jwt_required()
def admin_get_parking_areas():
    current_user_id = get_jwt_identity()
    # You can check if the current user is an admin before proceeding
    # Assuming is_admin is a field in User model or using a role-based system
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({"message": "Unauthorized access"}), 403

    parking_areas = ParkingArea.query.all()
    result = []
    for area in parking_areas:
        result.append({
            "id": area.id,
            "name": area.name,
            "location": area.location,
            "available_slots": area.available_slots
        })

    return jsonify(result)

# Admin route to add a new parking area
@main.route('/admin/parking-area', methods=['POST'])
@jwt_required()
def admin_add_parking_area():
    current_user_id = get_jwt_identity()
    # Check if the current user is an admin
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({"message": "Unauthorized access"}), 403

    data = request.get_json()

    name = data.get('name')
    location = data.get('location')
    available_slots = data.get('available_slots')

    try:
        new_parking_area = ParkingArea(name=name, location=location, available_slots=available_slots)
        db.session.add(new_parking_area)
        db.session.commit()

        return jsonify({"message": "Parking area added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding parking area", "error": str(e)}), 500
