# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()

login_manager = LoginManager()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cluster_api_address = db.Column(db.String(300), nullable=False)
    data_center_location = db.Column(db.String(120), unique=True, nullable=False)
    cluster_type = db.Column(db.String(120), unique=True, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))