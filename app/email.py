# from flask import current_app
# from flask_mail import Message, Mail
# from threading import Thread
# import os

# # Initialize Flask-Mail
# mail = Mail()

# def send_async_email(app, msg):
#     """Helper function to send emails in a separate thread"""
#     with app.app_context():
#         mail.send(msg)

# def send_confirmation_email(user_email):
#     """Function to send a confirmation email to the user after signup"""
#     subject = "Account Confirmation"
#     sender_email = current_app.config['MAIL_USERNAME']
#     recipient_email = user_email
    
#     # Compose the email body
#     body = f"""
#     Dear User,

#     Thank you for signing up!

#     Your account has been created successfully.

#     Regards,
#     Parking Management Team
#     """
    
#     msg = Message(subject, sender=sender_email, recipients=[recipient_email])
#     msg.body = body
    
#     # Send the email asynchronously
#     Thread(target=send_async_email, args=(current_app, msg)).start()

# def send_error_email(error_details):
#     """Function to send an error email to the admin (optional)"""
#     subject = "Error in Parking System"
#     sender_email = current_app.config['MAIL_USERNAME']
#     recipient_email = current_app.config['ADMIN_EMAIL']  # You can set an admin email in the .env file
    
#     # Compose the email body
#     body = f"""
#     An error occurred in the parking management system:

#     {error_details}

#     Please investigate the issue.

#     Regards,
#     Parking Management System
#     """
    
#     msg = Message(subject, sender=sender_email, recipients=[recipient_email])
#     msg.body = body
    
#     # Send the error email asynchronously
#     Thread(target=send_async_email, args=(current_app, msg)).start()

from flask_mail import Message, Mail
from threading import Thread
import os

# Initialize Flask-Mail
mail = Mail()

def send_async_email(app, msg):
    """Helper function to send emails in a separate thread"""
    with app.app_context():
        mail.send(msg)

def send_confirmation_email(user_email):
    """Function to send a confirmation email to the user after signup"""
    from flask import current_app  # Import here to avoid circular import
    
    subject = "Account Confirmation"
    sender_email = current_app.config['MAIL_USERNAME']
    recipient_email = user_email
    
    # Compose the email body
    body = f"""
    Dear User,

    Thank you for signing up!

    Your account has been created successfully.

    Regards,
    Parking Management Team
    """
    
    msg = Message(subject, sender=sender_email, recipients=[recipient_email])
    msg.body = body
    
    # Send the email asynchronously
    Thread(target=send_async_email, args=(current_app, msg)).start()

def send_error_email(error_details):
    """Function to send an error email to the admin (optional)"""
    from flask import current_app  # Import here to avoid circular import
    
    subject = "Error in Parking System"
    sender_email = current_app.config['MAIL_USERNAME']
    recipient_email = current_app.config['ADMIN_EMAIL']  # You can set an admin email in the .env file
    
    # Compose the email body
    body = f"""
    An error occurred in the parking management system:

    {error_details}

    Please investigate the issue.

    Regards,
    Parking Management System
    """
    
    msg = Message(subject, sender=sender_email, recipients=[recipient_email])
    msg.body = body
    
    # Send the error email asynchronously
    Thread(target=send_async_email, args=(current_app, msg)).start()
    