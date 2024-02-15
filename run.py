from app import app, db
from app.models import User

# Create the application context
with app.app_context():
    # Create all database tables
    db.create_all()

    # Check if the admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Create the admin user
        admin_user = User(username='admin', email='eimtingwi@gmail.com', is_admin=True)
        admin_user.set_password('vanawsum')
        admin_user.set_phone_number('+265996393991')  # Setting admin's phone number with country code
        db.session.add(admin_user)
        db.session.commit()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)