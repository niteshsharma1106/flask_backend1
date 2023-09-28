# views/cluster.py

from flask import Blueprint, render_template, redirect, request,session,flash
from models import db, Cluster, User,Trident,TridentSecret
from views.auth import login_required



cluster_bp = Blueprint('cluster', __name__)

@cluster_bp.route('/add_cluster', methods=['GET', 'POST'])
def add_cluster():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'Admin':
            if request.method == 'POST':
                dcloc = request.form['data_center_location']
                ctype = request.form['cluster_env']
                cenvironment = request.form['cluster_type']
                clusterapi = request.form['cluster_api_address']
                cluster = Cluster(dcloc=dcloc, ctype=ctype, clusterapi=clusterapi,cenvironment=cenvironment)
                trident = Trident(cluster_id=cluster.id,svmname='',dataLF='')
                tridentsecret = TridentSecret(cluster_id=cluster.id,password_en='',public_key='',pvt_key='')
                # Check if the cluster_api_address already exists in the database
                existing_cluster = Cluster.query.filter_by(clusterapi=clusterapi).first()
                if existing_cluster:
                    flash('Cluster API address already exists.', 'error')
                    print(f'Cluster API address {clusterapi} already exists.', 'error')
                    # Handle duplicate cluster_api_address (e.g., display an error message)
                    # For simplicity, we redirect back to the add_cluster page
                    return redirect('/add_cluster')
                cluster.tridents.append(trident)
                cluster.tridentsecrets.append(tridentsecret)
                db.session.add(cluster)
                db.session.commit()
            clusters = Cluster.query.all()
            return render_template('add_cluster.html', clusters=clusters)
        else:
            print(f'user {user} is not Admin to add or Remove cluster')
            flash('Only Admin can remove the details')
            return redirect('/welcome')
    else:
        return redirect('/login')

@cluster_bp.route('/remove_cluster/<int:cluster_id>', methods=['GET', 'POST'])
def remove_cluster(cluster_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user.role.name == 'Admin':
            trident = Trident.query.get_or_404(cluster_id)
            tridentsecret = TridentSecret.query.get_or_404(cluster_id)
            cluster = Cluster.query.get_or_404(cluster_id)
            db.session.delete(trident)
            db.session.delete(tridentsecret)
            db.session.delete(cluster)
            db.session.commit()
            # After deleting rows, reset the auto-increment counter
        else:
            print(f'user {user} is not admin')
            flash('Only Admin can remove the details')
    else:
        return redirect('/login')
    return redirect('/add_cluster')
