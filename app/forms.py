from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, NumberRange
from app.models import User, RestaurantTable


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')


class AddTableForm(FlaskForm):
    status = SelectField('Status', choices=[('Available', 'Available'), ('Reserved', 'Reserved')], validators=[DataRequired()])
    submit = SubmitField('Add Table')


class ReservationForm(FlaskForm):
    table_id = SelectField('Table', coerce=int, validators=[InputRequired()])
    number_of_guests = IntegerField('Number of Guests', validators=[InputRequired(), NumberRange(min=1)])
    occasion = StringField('Occasion', validators=[InputRequired()])
    submit = SubmitField('Make Reservation')

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.table_id.choices = [(table.table_id, str(table.table_id)) for table in RestaurantTable.query.filter_by(status='Available').all()]

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(min=4, max=100)])
    whatsapp_number = StringField('WhatsApp Number', validators=[Length(max=20)])
    submit = SubmitField('Update Profile')