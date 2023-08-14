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

    # if request.method == 'POST':
    #     cluster_api = request.form['cluster_api']
    #     svm_name = request.form['svm_name']
    #     dataLF = request.form['dataLF']
    #     last_password_updated_on = request.form['last_password_updated_on']

    #     # Create or update the Trident_Data entry
    #     trident_entry = Trident.query.first()
    #     if not trident_entry:
    #         trident_entry = Trident()
    #         db.session.add(trident_entry)
    #     trident_entry.cluster_api_address_id = Cluster.query.filter_by(cluster_api_address=cluster_api).first().id
    #     trident_entry.svm_name = svm_name
    #     trident_entry.dataLF = dataLF
    #     trident_entry.last_password_updated_on = last_password_updated_on
    #     db.session.commit()

    #     flash('Trident Data updated successfully.', 'success')

    # Get all the entries from Trident_Data table
    trident_entries = Trident.query.all()
    print(trident_entries)

    return render_template('trident.html', trident_entries=trident_entries)

