# views/cluster.py

from flask import Blueprint, render_template, redirect, request,session,flash
from models import db, Cluster
from views.auth import login_required



cluster_bp = Blueprint('cluster', __name__)

@cluster_bp.route('/add_cluster', methods=['GET', 'POST'])
def add_cluster():
    if 'user_id' in session:
        if request.method == 'POST':
            data_center_location = request.form['data_center_location']
            cluster_type = request.form['cluster_type']
            cluster_api_address = request.form['cluster_api_address']
            cluster = Cluster(data_center_location=data_center_location, cluster_type=cluster_type, cluster_api_address=cluster_api_address)
            # Check if the cluster_api_address already exists in the database
            existing_cluster = Cluster.query.filter_by(cluster_api_address=cluster_api_address).first()

            if existing_cluster:
                flash('Cluster API address already exists.', 'error')
                print(f'Cluster API address {cluster_api_address} already exists.', 'error')
                # Handle duplicate cluster_api_address (e.g., display an error message)
                # For simplicity, we redirect back to the add_cluster page
                return redirect('/add_cluster')
            db.session.add(cluster)
            db.session.commit()
        clusters = Cluster.query.all()
        return render_template('add_cluster.html', clusters=clusters)
    else:
        return redirect('/login')

@cluster_bp.route('/remove_cluster/<int:cluster_id>', methods=['GET', 'POST'])
def remove_cluster(cluster_id):
    if 'user_id' in session:
        
        cluster = Cluster.query.get_or_404(cluster_id)
        db.session.delete(cluster)
        db.session.commit()
        # After deleting rows, reset the auto-increment counter
    else:
        return redirect('/login')
    return redirect('/add_cluster')
