# views/home.py

from flask import Blueprint, render_template,session,redirect
from flask_login import login_required


home_bp = Blueprint('home', __name__)


@home_bp.route('/welcome')
def welcome():
    # Check if the user is logged in (session variable 'user_id' is set)
    if 'user_id' in session:
        user_name = session.get('user_name', 'Guest') 
        print(user_name)
        return render_template('home.html',user_name=user_name)
    else:
        return redirect('/login')