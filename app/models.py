from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)  

    reservations = db.relationship('Reservation', back_populates='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)

    def set_phone_number(self, phone):
        phone_pattern = re.compile(r'^\+\d{1,3}\d{9,15}$')  # Assuming country code followed by 9-15 digits
        if not phone_pattern.match(phone):
            raise ValueError("Invalid phone number format. It should start with a '+' followed by country code and then the phone number.")
        
        self.phone_number = phone

class RestaurantTable(db.Model):
    table_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='Available')

    reservations = db.relationship('Reservation', back_populates='table', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<RestaurantTable {self.table_id}>'

    @property
    def has_reserved_reservations(self):
        return any(reservation.status == 'Reserved' for reservation in self.reservations)

class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    number_of_guests = db.Column(db.Integer, nullable=False)
    occasion = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('restaurant_table.table_id'), nullable=False)

    user = db.relationship('User', back_populates='reservations')
    table = db.relationship('RestaurantTable', back_populates='reservations')

    def __repr__(self):
        return f'<Reservation {self.reservation_id}>'
