# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy import text, event, ForeignKey
from datetime import datetime, timedelta

db = SQLAlchemy()

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    __tablename__ = 'cluster'

    id = db.Column(db.Integer, primary_key=True)
    clusterapi = db.Column(db.String(200),unique=True,nullable=False)
    #dctype = db.Column(db.String(200),nullable=False)
    dcloc = db.Column(db.String(200),nullable=False)
    ctype = db.Column(db.String(200),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    tridents = db.relationship('Trident', back_populates='cluster')

    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
class Trident(db.Model):
    __tablename__ = 'trident'
    
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)
    svmname = db.Column(db.String(200),nullable=True)
    dataLF = db.Column(db.String(200),nullable=True)
    last_password_updated_on = db.Column(db.DateTime, default=datetime.now())
    cluster = db.relationship('Cluster', back_populates='tridents')

    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


