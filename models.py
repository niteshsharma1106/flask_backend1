# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy import text

db = SQLAlchemy()

login_manager = LoginManager()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_center_location = db.Column(db.String(120), nullable=False)
    cluster_type = db.Column(db.String(120), nullable=False)
    cluster_api_address = db.Column(db.String(300), nullable=False,unique=True)
    serial_number = db.Column(db.Integer, nullable=False, default=0)
    def save(self):
        if not self.id:
            # Generate the next sequential number when saving a new record
            last_cluster = Cluster.query.order_by(Cluster.serial_number.desc()).first()
            self.serial_number = 1 if not last_cluster else last_cluster.serial_number + 1
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        # Recalculate sequential numbers after deleting a record
        clusters = Cluster.query.order_by(Cluster.serial_number.asc()).all()
        for i, cluster in enumerate(clusters, 1):
            cluster.serial_number = i
        db.session.commit()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
