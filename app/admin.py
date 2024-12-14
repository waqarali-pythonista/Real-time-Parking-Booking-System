from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import ParkingArea, User, Booking
from app.email import send_confirmation_email

# Create a blueprint for admin routes
admin = Blueprint('admin', __name__, url_prefix='/admin')

# Route to add a new parking area
@admin.route('/add_parking_area', methods=['POST'])
def add_parking_area():
    """
    Adds a new parking area to the system.
    """
    data = request.get_json()
    try:
        name = data['name']
        location = data['location']
        
        # Create a new ParkingArea object
        new_parking_area = ParkingArea(name=name, location=location)
        
        # Add to the database
        db.session.add(new_parking_area)
        db.session.commit()
        
        return jsonify({'message': 'Parking area added successfully', 'id': new_parking_area.id}), 201
    except Exception as e:
        current_app.logger.error(f"Error adding parking area: {e}")
        return jsonify({'message': 'Error adding parking area', 'error': str(e)}), 400

# Route to view all parking areas
@admin.route('/view_parking_areas', methods=['GET'])
def view_parking_areas():
    """
    Returns a list of all parking areas.
    """
    parking_areas = ParkingArea.query.all()
    
    # Convert parking areas to dictionary for easy JSON response
    areas_list = [area.to_dict() for area in parking_areas]
    
    return jsonify({'parking_areas': areas_list}), 200

# Route to view all users
@admin.route('/view_users', methods=['GET'])
def view_users():
    """
    Returns a list of all users in the system.
    """
    users = User.query.all()
    
    # Convert users to dictionary for easy JSON response
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    
    return jsonify({'users': users_list}), 200

# Route to view all bookings
@admin.route('/view_bookings', methods=['GET'])
def view_bookings():
    """
    Returns a list of all bookings.
    """
    bookings = Booking.query.all()
    
    # Convert bookings to dictionary for easy JSON response
    bookings_list = [{'id': booking.id, 'user_id': booking.user_id, 
                      'parking_slot_id': booking.parking_slot_id, 'booked_at': booking.booked_at} 
                     for booking in bookings]
    
    return jsonify({'bookings': bookings_list}), 200

# Route to delete a parking area (admin only)
@admin.route('/delete_parking_area/<int:id>', methods=['DELETE'])
def delete_parking_area(id):
    """
    Deletes a parking area by ID.
    """
    parking_area = ParkingArea.query.get(id)
    
    if parking_area:
        try:
            db.session.delete(parking_area)
            db.session.commit()
            return jsonify({'message': 'Parking area deleted successfully'}), 200
        except Exception as e:
            current_app.logger.error(f"Error deleting parking area: {e}")
            return jsonify({'message': 'Error deleting parking area', 'error': str(e)}), 400
    else:
        return jsonify({'message': 'Parking area not found'}), 404
