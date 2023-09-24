# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy import text, event, ForeignKey,String
from datetime import datetime, timedelta,date
from sqlalchemy.orm import Mapped,mapped_column,relationship,DeclarativeBase

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
        app_admin_role = Role.query.filter_by(name='App_Admin').first()

        # Create default roles if they don't exist
        if not admin_role:
            admin_role = Role(name='Admin')
            db.session.add(admin_role)

        if not view_role:
            view_role = Role(name='View')
            db.session.add(view_role)
        
        if not app_admin_role:
            app_admin_role = Role(name='App_Admin')
            db.session.add(app_admin_role)

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
    dcloc = db.Column(db.String(200),nullable=False)
    ctype = db.Column(db.String(200),nullable=False)
    cenvironment = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime, default=date.today())
    # Define a one-to-many relationship with Trident
    tridents = db.relationship('Trident', back_populates='cluster')
    # Define a one-to-many relationship with TridentSecret
    tridentsecrets = db.relationship('TridentSecret', back_populates='cluster', lazy='dynamic')
    # Define a one-to-many relationship with Inventory
    invontory_use = db.relationship('Inventory', back_populates="cluster",lazy='dynamic')

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
    last_password_updated_on = db.Column(db.DateTime, default=date.today())
    cluster = db.relationship('Cluster', back_populates='tridents')

    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TridentSecret(db.Model):
    __tablename__ = 'tridentsecret'

    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)
    password_en = db.Column(db.String,nullable=False)
    public_key = db.Column(db.String,nullable=False)
    pvt_key = db.Column(db.String,nullable=False)
    last_updated =  db.Column(db.DateTime, default=date.today(),onupdate=datetime)
    cluster = db.relationship('Cluster', back_populates='tridentsecrets')
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Inventory(db.Model):
    __tablename__ = 'invontory'

    id = db.Column(db.Integer,primary_key=True)
    nodename = db.Column(db.String(100),unique=True)
    node_ip = db.Column(db.String(64),unique=True)
    node_role = db.Column(db.String,unique=False)
    node_state =  db.Column(db.String(20),unique=False)
    cluster_id = db.Column(db.Integer,db.ForeignKey("cluster.id"),nullable=False)
    cluster = db.relationship('Cluster', back_populates="invontory_use")
    update_on =  db.Column(db.DateTime,default=date.today(), onupdate=datetime)

    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



