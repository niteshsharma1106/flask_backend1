# run.py

from flask import Flask
from config import DATABASE_URI
from models import db, login_manager,Role,User,Inventory
from views.auth import auth_bp
from views.home import home_bp
from views.ocpcluster import cluster_bp
from views.admin import admin_bp
from views.trident import trident_bp
from views.inventory import inventory_bp
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set a secret key for the session management
app.config['SECRET_KEY'] = '11002355'

db.init_app(app)

# Set up flask_login
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # The route for the login page


# Create all the database tables
with app.app_context():
    db.create_all()
    Role.create_default_roles()
        # Check if there are any users in the database
    if not User.query.first():
        # If no users exist, create the default admin role
        admin_role = Role.query.filter_by(name='Admin').first()
        if not admin_role:
            admin_role = Role(name='Admin')
            db.session.add(admin_role)
            db.session.commit()

        # Create the default admin user
        default_admin_user = User(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password='password',  # Replace with the desired default password
            role=admin_role,
            force_password_change=True  # Set this flag to force password change on first login
        )
        db.session.add(default_admin_user)
        db.session.commit()

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(cluster_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(trident_bp)
app.register_blueprint(inventory_bp)

if __name__ == '__main__':
    from waitress import serve
    #serve(app, host="127.0.0.1", port=5000)
    app.run(debug=True)
    