# views/admin.py

from flask import Blueprint, render_template, redirect, request, session,flash
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
def approve_request(request_id):
    print('Approve',request_id)
    if session['user_id']:
        print('to Approve',request_id)
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'Admin':
            print('Admin to Approve',request_id)
            access_request = AccessRequest.query.get(request_id)
            user = access_request.user
            role_id = access_request.role_id
            user.role_id = role_id
            db.session.commit()
            access_request.approved = True
            # user_st = User.query.get(request_id)
            # user_st.role_id = session
            db.session.commit()
            flash("Access request approved successfully.")
        else:
            flash("You don't have permission to approve requests.")
            return redirect('welcome')
    return redirect('/access_requests')

@admin_bp.route('/deny_request/<int:request_id>', methods=['POST'])
def deny_request(request_id):
    print('Deny',request_id)
    if session['user_id']:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'Admin':
            access_request = AccessRequest.query.get(request_id)
            user_id = access_request.user_id
            user_del = User.query.get(user_id)
            db.session.delete(access_request)
            db.session.delete(user_del)  # Delete the user object associated with the access request
            db.session.commit()
            flash("Access request denied and user removed.")

        else:
            flash("Administrator Only!")
            return redirect('welcome')
    return redirect('/access_requests')

