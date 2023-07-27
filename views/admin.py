# views/admin.py

from flask import Blueprint, render_template, redirect, request, session
from models import db, User, AccessRequest, Role
from views.auth import login_required

admin_bp = Blueprint('admin_access', __name__)

@admin_bp.route('/access_requests')
#@login_required
def access_requests():
    user_id = session['user_id']
    print(f'from access request {session["user_id"]} and user {User.query.get(user_id).first_name}')
    if session['user_id']:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'Admin':
            print(f'from access request {session["user_id"]} and user {User.query.get(user_id).first_name}')
            access_requests = AccessRequest.query.filter_by(approved=False).all()
            return render_template('access_requests.html', access_requests=access_requests)
    return redirect('/welcome')


@admin_bp.route('/approve_request/<int:request_id>', methods=['POST'])
#@login_required
def approve_request(request_id):
    if session['user_id']:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'admin':
            access_request = AccessRequest.query.get(request_id)
            access_request.approved = True
            db.session.commit()
    return redirect('/access_requests')

@admin_bp.route('/deny_request/<int:request_id>', methods=['POST'])
#@login_required
def deny_request(request_id):
    if session['user_id']:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'admin':
            access_request = AccessRequest.query.get(request_id)
            db.session.delete(access_request)
            db.session.commit()
    return redirect('/access_requests')

