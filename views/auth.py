# views/auth.py

from flask import Blueprint, render_template, redirect, request,session,flash
from flask_login import login_required, current_user, LoginManager
from models import db, User,login_manager,Role,AccessRequest

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('home.html')

@auth_bp.route('/welcome')
def welcome():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        #print(user,user.force_password_change)
        if user.force_password_change:
            # If the force_password_change flag is True, redirect to the change_password route
            return redirect('/change_password')
        return render_template('welcome.html')
    else: 
        return redirect('/login')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    roles = Role.query.all()  # Get all available roles
    print(f'List of roles: {roles}')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role_id = int(request.form['role'])  # Get the selected role ID from the form
        role = request.form['role'] # Get the role object based on the selected ID

        # Create an access request for the selected role
        # new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, role_id=role_id)
        # db.session.add(new_user)

        # Create an access request for the selected role
        access_request = AccessRequest(user=User(first_name=first_name, last_name=last_name, email=email, password=password),
                                       role_id=role_id)
        db.session.add(access_request)
        db.session.commit()
        # access_request = AccessRequest(user=new_user, role_id=role_id)
        # db.session.add(access_request)
        # db.session.commit()
        # Redirect to a confirmation page or display a message indicating that the request is pending approval
        return redirect('/registration_pending')
        # return redirect('/login') 
    return render_template('register.html', roles=roles)

@auth_bp.route('/registration_pending')
def registration_pending():
    # Display a message or a separate page indicating that the registration is pending approval
    return render_template('registration_pending.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        #print(f'login {user.role}')
        if user and user.role is not None and user.email is not None:
            
            # Set a session variable to indicate that the user is logged in
            session['user_id'] = user.id
            # You can add a session here for managing user login status
            # Store the user's name in the session
            session['user_name'] = user.first_name
            return redirect('/welcome')
        else:
            flash("Your are Not Yet Authorised to login!!\nContact Application Administrator!")


    return render_template('login.html')


@auth_bp.route('/logout')
# @login_required  # Apply the login_required decorator
def logout():
    # Clear the session to log the user out
    session.clear()
    return redirect('/welcome')

@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' in session:
        if request.method == 'POST':
            user = User.query.get(session['user_id'])
            new_password = request.form['new_password']
            user.password = new_password
            user.force_password_change = False  # Set the flag to False after changing the password
            db.session.commit()
            return redirect('/welcome')
    return render_template('change_password.html')