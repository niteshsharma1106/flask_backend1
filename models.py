# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy import text

db = SQLAlchemy()

login_manager = LoginManager()



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    @staticmethod
    def create_default_roles():
        # Check if the default roles already exist in the database
        admin_role = Role.query.filter_by(name='Admin').first()
        view_role = Role.query.filter_by(name='View').first()

        # Create default roles if they don't exist
        if not admin_role:
            admin_role = Role(name='Admin')
            db.session.add(admin_role)

        if not view_role:
            view_role = Role(name='View')
            db.session.add(view_role)

        db.session.commit()



class AccessRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='access_requests')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role')
    approved = db.Column(db.Boolean, default=False)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    role = db.relationship('Role', backref='users')
    force_password_change = db.Column(db.Boolean, default=True)

    def save(self):
        if not self.id:
            # ... (same code)
            # Save the user and set the password change flag to True
            self.force_password_change = True
            db.session.add(self)
            db.session.commit()



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
