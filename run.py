# run.py

from flask import Flask
from config import DATABASE_URI
from models import db
from views.auth import auth_bp
from views.home import home_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set a secret key for the session management
app.config['SECRET_KEY'] = '11002355'

db.init_app(app)

# Create all the database tables
with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

if __name__ == '__main__':
    app.run(debug=True)

nitesh