# views/inventory.py

from flask import Blueprint, render_template, redirect, request, session, flash
from models import db, Cluster, User, Trident,Inventory
from views.auth import login_required
import datetime
from datetime import date

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory_view', methods=['GET', 'POST'])
def inventory_view():
    # Check if the user is an admin
    user_id = session['user_id']
    user = User.query.get(user_id)
    if user.role.name != 'Admin':
        flash('You need to be an admin to access this page.', 'error')
        return redirect('/welcome')
    cluster_entries = Cluster.query.order_by(Cluster.clusterapi).all()
    print(cluster_entries)
    return render_template('inventory_view.html', cluster_entries=cluster_entries)


@inventory_bp.route('/inventory_fetch', methods=['POST'])
def inventory_fetch():
    if session['user_id']:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'Admin':
            print(request.form.items)
            print('calling inventory function to fetch')
            flash("Access request approved successfully.")
        else:
            flash("You don't have permission to approve requests.")
            return redirect('welcome')
    return redirect('/inventory_view')