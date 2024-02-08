# Import necessary modules
from flask import render_template
from flask_mail import Message
from app import mail

def send_reservation_email(admin_email, reservation):
    subject = 'New Reservation'
    recipients = [admin_email]
    body = render_template('email_templates/reservation_email.html', reservation=reservation)
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)
