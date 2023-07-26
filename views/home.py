# views/home.py

from flask import Blueprint, render_template,session,redirect


home_bp = Blueprint('home', __name__)


@home_bp.route('/welcome')
def welcome():
    # Check if the user is logged in (session variable 'user_id' is set)
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/login')