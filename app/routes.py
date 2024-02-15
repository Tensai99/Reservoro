from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, login_manager
from app.forms import LoginForm, SignupForm, AddTableForm, ReservationForm, ProfileForm
from app.models import User, RestaurantTable, Reservation
from datetime import datetime, date
from app.mail import send_email

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel')) if current_user.is_admin else redirect(url_for('make_reservation'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel')) if current_user.is_admin else redirect(url_for('make_reservation'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_panel')) if user.is_admin else redirect(url_for('make_reservation'))
        flash('Invalid username or password', 'danger')  # Add flash message for invalid login
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        if form.phone_number.data:
            try:
                user.set_phone_number(form.phone_number.data)
            except ValueError as e:
                flash(str(e), 'danger')
                return redirect(url_for('signup'))
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('make_reservation'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    form = AddTableForm()

    try:
        if form.validate_on_submit():
            table = RestaurantTable(status=form.status.data)
            db.session.add(table)
            db.session.commit()
            flash('Table added successfully!', 'success')
            return redirect(url_for('admin_panel'))

        tables = RestaurantTable.query.all()

        # Create a dictionary to store a form for each table
        table_forms = {table.table_id: AddTableForm() for table in tables}

        # Rest of your code...

        return render_template('admin_panel.html', tables=tables, form=form, table_forms=table_forms)

    except Exception as e:
        print(f"Error in admin_panel: {e}")
        db.session.rollback()
        flash('An error occurred. Please check the logs for details.', 'error')
        return render_template('error.html', error_message='An error occurred. Please try again later.')



"""@app.route('/admin/add_table', methods=['POST'])
@login_required
def add_table():
    if not current_user.is_admin:
        return redirect(url_for('make_reservation'))

    form = AddTableForm()
    if form.validate_on_submit():
        status = form.status.data
        table = RestaurantTable(status=status)
        db.session.add(table)
        db.session.commit()
        flash('Table added successfully!', 'success')
    else:
        flash('Invalid input!', 'error')

    return redirect(url_for('admin_panel'))
"""

@app.route('/update_table_status/<int:table_id>/<string:new_status>', methods=['POST'])
@login_required
def update_table_status(table_id, new_status):
    try:
        table = RestaurantTable.query.get(table_id)

        if table:
            table.status = new_status

            # Update the reservation details if the new status is "Available"
            if new_status == 'Available':
                reservations = Reservation.query.filter_by(table_id=table_id).all()
                for reservation in reservations:
                    reservation.date = None
                    reservation.time = None

            db.session.commit()
            flash(f'Table {table_id} status changed to {new_status}.', 'success')
        else:
            flash(f'Table {table_id} not found.', 'error')

    except Exception as e:
        print(f"Error during table status update: {e}")
        db.session.rollback()
        flash('Error updating table status. Please check the logs for details.', 'error')
        raise

    return redirect(url_for('admin_panel'))


@app.route('/update_reservation_status', methods=['POST'])
@login_required
def update_reservation_status():
    table_id = int(request.form.get('table_id'))
    reservation_id = int(request.form.get('reservation_id'))
    new_status = request.form.get('new_status')

    table = RestaurantTable.query.get(table_id)
    if table:
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            reservation.status = new_status
            db.session.commit()
            flash('Reservation status updated successfully!', 'success')

            # If the new status is "Available," remove the reservation from the table
            if new_status == 'Available':
                table.reservations.remove(reservation)
                db.session.commit()
        else:
            flash('Reservation not found!', 'danger')
    else:
        flash(f'Table {table_id} not found.', 'error')

    return redirect(url_for('admin_panel'))

def get_admin_email():
    admin = User.query.filter_by(is_admin=True).first()
    if admin:
        return admin.email
    else:
        return None

@app.route('/make_reservation', methods=['GET', 'POST'])
@login_required
def make_reservation():
    if current_user.is_admin:
        return redirect(url_for('admin_panel'))

    current_date = date.today()

    tables = RestaurantTable.query.all()

    form = ReservationForm()
    form.table_id.choices = [(str(table.table_id), str(table.table_id)) for table in tables]

    if form.validate_on_submit():
        table_id = int(form.table_id.data)
        number_of_guests = form.number_of_guests.data
        occasion = form.occasion.data
        reservation_datetime = datetime.strptime(request.form['reservation_datetime'], '%Y-%m-%d %H:%M')

        table = RestaurantTable.query.get(table_id)
        if table:
            conflicting_reservation = Reservation.query.filter_by(date=reservation_datetime.date(),
                                                                  table_id=table_id).first()
            if conflicting_reservation:
                if conflicting_reservation.time == reservation_datetime.time():
                    flash('The selected table and time are already booked. Please select a different time.', 'danger')
                else:
                    table.status = 'Reserved'
                    db.session.commit()

                    reservation = Reservation(
                        date=reservation_datetime.date(),
                        time=reservation_datetime.time(),
                        number_of_guests=number_of_guests,
                        occasion=occasion,
                        user_id=current_user.user_id,
                        table_id=table_id
                    )
                    db.session.add(reservation)
                    db.session.commit()

                    # Send confirmation email
                    sender = get_admin_email()
                    if sender:
                        recipient = current_user.email
                        subject = "Reservation Confirmation"
                        body = f"Your reservation details:\nTable ID: {table_id}\nNumber of Guests: {number_of_guests}\nOccasion: {occasion}\nDate: {reservation_datetime.date()}\nTime: {reservation_datetime.time()}"
                        send_email(sender, recipient, subject, body)
                    else:
                        flash('Failed to send confirmation email. Admin email not found.', 'error')

                    return redirect(url_for('make_reservation'))
            else:
                table.status = 'Reserved'
                db.session.commit()

                reservation = Reservation(
                    date=reservation_datetime.date(),
                    time=reservation_datetime.time(),
                    number_of_guests=number_of_guests,
                    occasion=occasion,
                    user_id=current_user.user_id,
                    table_id=table_id
                )
                db.session.add(reservation)
                db.session.commit()

                # Send confirmation email
                sender = get_admin_email()
                if sender:
                    recipient = current_user.email
                    subject = "Reservation Confirmation"
                    body = f"Your reservation details:\nTable ID: {table_id}\nNumber of Guests: {number_of_guests}\nOccasion: {occasion}\nDate: {reservation_datetime.date()}\nTime: {reservation_datetime.time()}"
                    send_email(sender, recipient, subject, body)
                else:
                    flash('Failed to send confirmation email. Admin email not found.', 'error')

                return redirect(url_for('make_reservation'))
        else:
            flash('Table not found.', 'danger')

    reservations = current_user.reservations

    return render_template('make_reservation.html', form=form, tables=tables, reservations=reservations, current_date=current_date)


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    
    if reservation:
        # Check if the reservation belongs to the current user
        if reservation.user_id == current_user.user_id:
            # Update the table status to "Available"
            table = reservation.table
            table.status = "Available"
            db.session.commit()

            # Delete the reservation from the database
            db.session.delete(reservation)
            db.session.commit()
            flash('Reservation canceled successfully.', 'success')
        else:
            flash('You are not authorized to cancel this reservation.', 'error')
    else:
        flash('Reservation not found.', 'error')
    
    return redirect(url_for('make_reservation'))

@app.route('/check_availability', methods=['POST'])
def check_availability():
    table_id = request.form.get('table_id')
    reservation_datetime = datetime.strptime(request.form.get('reservation_datetime'), '%Y-%m-%dT%H:%M')

    table = RestaurantTable.query.get(table_id)
    if table:
        conflicting_reservation = Reservation.query.filter_by(date=reservation_datetime.date(),
                                                              time=reservation_datetime.time(),
                                                              table_id=table_id).first()
        if conflicting_reservation:
            return jsonify(available=False)
        else:
            return jsonify(available=True)
    else:
        return jsonify(available=False)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Profile', form=form)