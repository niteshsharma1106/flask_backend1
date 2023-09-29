# views/trident.py

from flask import Blueprint, render_template, redirect, request, session, flash,jsonify
from models import db, Cluster, User, Trident,TridentSecret
from views.auth import login_required
import datetime
from datetime import date, datetime
import json
import subprocess
trident_bp = Blueprint('trident', __name__)

#Create new Cluster and Trident_Data records with a relationship


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
            print('--->',trident_request.last_password_updated_on)
            clusterapi = trident_request.cluster.clusterapi
            print(f'Request to fetch for Cluster : {clusterapi}')
            data = fetch_trident_data()
            last_update = data[clusterapi]['last_updated']
            datetime_object = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S.%f")
            print(type(last_update))
            trident_request.last_password_updated_on = datetime_object
            db.session.flush()
            db.session.commit()
            flash("Access request approved successfully.")
        else:
            flash("You don't have permission to approve requests.")
            return redirect('welcome')
    return redirect('/trident_data_view')


@trident_bp.route('/reset_password/<int:entry_id>', methods=['POST'])
def reset_password(entry_id):
    trident_request = Trident.query.get(entry_id)
    
    command = ['python', 'D:\/vCodes\/trident_ss\main.py', f'{trident_request.cluster.clusterapi}']
    print(f"Rest Password for cluster : {trident_request.cluster.clusterapi}, command is {command}")
    try:
        # Run the command
        subprocess.run(command, check=True)
        return jsonify({'Process':'Reset Process is started kindly check the logs at server'})
    except subprocess.CalledProcessError as e:
        # Handle any errors or exceptions
        print(f"Error: {e}")
        return jsonify({'Error':'An Error Occured and password is not updated, Check server side error'})


def fetch_trident_data():
    with open('trident_secret.json') as secret_data:
        content = json.load(secret_data)
        secret_data.close
    print('Fetching Data for the required Cluster')
    for data in content:
        print(f"Last Update Password for Cluster {data} is {content[data]['last_updated']}")
    return content



#fetch_trident_data()