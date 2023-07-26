# run.py

from flask import Flask
from config import DATABASE_URI
from models import db, login_manager
from views.auth import auth_bp
from views.home import home_bp
from views.ocpcluster import cluster_bp
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

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(cluster_bp)

if __name__ == '__main__':
    app.run(debug=True)