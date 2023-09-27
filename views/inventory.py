# views/inventory.py

from flask import Blueprint, render_template, redirect, request, session, flash
from models import db, Cluster, User
from views.auth import login_required
import datetime
from datetime import date
import login
from kubernetes import client
inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory_view', methods=['GET'])
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
    if request.method == 'POST' :
        print('From inventory fetch method', request.form.get('c_fetch'))
        if session['user_id']:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user.role.name == 'Admin':
                nodes_info = fetch_inv_auth('https://api.n1okd-pclus03.india.airtel.itm:6443')  #(request.form.get('c_fetch'))
                print('calling inventory function to fetch')
                flash("Access request approved successfully.")
                cluster_entries = Cluster.query.order_by(Cluster.clusterapi).all()
                return render_template('inventory_view.html', cluster_entries=cluster_entries, nodes_info=nodes_info)
            else:
                flash("You don't have permission to approve requests.")
                return redirect('welcome')
    return redirect('/inventory_view')

def fetch_inv_auth(clusterapi):
    oc_dyn_client = login.get_dyn_oc_client(clusterapi)
    if oc_dyn_client == 0:
        '''Return if Authorization failed'''
        result = {
            "cluster_url": clusterapi,
            'error': 'Authorization failed'
            }
        return 0
    else:
        nodal_list = fetch_inv_from_cluster(oc_dyn_client)
        return nodal_list


def fetch_inv_from_cluster(oc_dyn_client):      
        nodes = oc_dyn_client.resources.get(api_version='v1', kind='Node')
        try:
            #logging.debug(f'Checking if project {project_name} is already present'.title())
            node_data = nodes.get()
            node_data = node_data
            #print("-------->",[data['metadata']['name'] for data in node_data.items])
                  #node_data.items[0].keys())
            nodes_info = extract_node_info(node_data)
            #print("Node Information:",nodes_info)
            for val in nodes_info:
                 print(f"{val}")
            return nodes_info
            ## also add login to check if Project with same RITM exits
            #existing_project_ritm = existing_project["metadata"]["annotations"]["openshift.io/ritm"]
        except client.exceptions.ApiException as e:
            if e.status != 404:
                print(f'Error Recieved: {e}')
                raise e
            return 0
        
def extract_node_info(node_data):
    nodes_info_list = []
    #[data['metadata']['name'] for data in node_data.items])
    for nodes_data in node_data.items:
        node_info = {}
        # Extract Name
        node_info['Name'] = nodes_data['metadata']['name']
        #print("====",node_info)
        # Extract IP Address (ExternalIP if available, otherwise InternalIP)
        addresses = nodes_data['status']['addresses']
        for address in addresses:
            if address['type'] == 'ExternalIP':
                node_info['IP_Address'] = address['address']
                break
        else:
            # If ExternalIP is not available, use InternalIP
            for address in addresses:
                if address['type'] == 'InternalIP':
                    node_info['IP_Address'] = address['address']
                    break

        # Extract Role (based on labels)
        labels = nodes_data['metadata']['labels']
        #print((labels.keys()))
        if 'node-role.kubernetes.io/worker' in labels.keys():
            node_info['Role'] = 'Worker'
        elif 'node-role.kubernetes.io/master' in labels.keys():
            node_info['Role'] = 'Master'
        else:
            node_info['Role'] = 'Unknown'

        # Extract Status (Ready/Not Ready)
        conditions = nodes_data['status']['conditions']
        for condition in conditions:
            if condition['type'] == 'Ready':
                node_info['Status'] = 'Ready' if condition['status'] == 'True' else 'Not Ready'
                break
        else:
            node_info['Status'] = 'Unknown'

        # Extract machineconfiguration.openshift.io/state
        annotations = nodes_data['metadata']['annotations']
        node_info['machineconfig_state'] = annotations.get(
            'machineconfiguration.openshift.io/state', 'N/A'
        )
        #print(node_info)
        #print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
        nodes_info_list.append(node_info)
    #print("11111111111111111111111",nodes_info)

    return nodes_info_list