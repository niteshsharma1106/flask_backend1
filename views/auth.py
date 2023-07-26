# views/auth.py

from flask import Blueprint, render_template, redirect, request,session
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('home.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:

            # Set a session variable to indicate that the user is logged in
            session['user_id'] = user.id
            # You can add a session here for managing user login status
            return redirect('/welcome')

    return render_template('login.html')
