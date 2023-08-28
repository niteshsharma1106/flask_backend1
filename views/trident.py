# views/trident.py

from flask import Blueprint, render_template, redirect, request, session, flash
from models import db, Cluster, User, Trident
from views.auth import login_required
import datetime

trident_bp = Blueprint('trident', __name__)

# Create new Cluster and Trident_Data records with a relationship


@trident_bp.route('/trident_data_view', methods=['GET', 'POST'])
def trident_data_view():
    # Check if the user is an admin
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user.role.name != 'Admin':
        flash('You need to be an admin to access this page.', 'error')
        return redirect('/welcome')
    trident_entries = Trident.query.all()
    print(trident_entries)

    return render_template('trident.html', trident_entries=trident_entries)


@trident_bp.route('/fetch_requests/<int:entry_id>', methods=['POST'])
def fetch_requests(entry_id):
    print('Approve',entry_id)
    if session['user_id']:
        print('to Approve',entry_id)
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'Admin':
            print('calling function to fetch',entry_id)
            trident_request = Trident.query.get(entry_id)
            clusterapi = trident_request.cluster.clusterapi
            print(f'Request to fetch for Cluster : {clusterapi}')
            flash("Access request approved successfully.")
        else:
            flash("You don't have permission to approve requests.")
            return redirect('welcome')
    return redirect('/trident_data_view')
