from kubernetes import client
from openshift.dynamic import DynamicClient
from openshift.helper.userpassauth import OCPLoginConfiguration
from openshift.helper.userpassauth import OCPLoginRequestException
import urllib3
import yaml
import logging


# Set up logging
logging.basicConfig(level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
USER_VAR = "reference_var"  #"inv//group_vars//reference_var"


def user_input_file():
    with open(USER_VAR, 'r') as user_input:
        user_input_read = yaml.safe_load(user_input)
    return user_input_read


def get_cluster_url(data_content, dc, env):
    try:
        return data_content[dc][env]
        #this will be list for url's
    except IndexError as e:
        print("List is empty", e)
    return None


class OCClient:
    def __init__(self, dc, env):
        self.var_file_content = user_input_file()   # this will get the content of the reference variable file
        self.dc = dc
        self.env = env

    def get_client(self, url):
        apihost = url
        username = self.var_file_content['htpass']['username']
        password = self.var_file_content['htpass']['password']
        kubeconfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
        kubeconfig.host = apihost
        kubeconfig.verify_ssl = False
        try:
            kubeconfig.get_token()

        except OCPLoginRequestException as e:
            print(f"Authorization failed: {e}")
            return {'dclient': 'Authorization failed', 'auth_key': 0, 'cluster_url': apihost}
        try:
            k8s_client = client.ApiClient(kubeconfig)
            logging.info('Auth token: {0}'.format(kubeconfig.api_key))
            logging.info('Token expires: {0}'.format(kubeconfig.api_key_expires))
            # Initialize the OpenShift client
            return {'dclient': DynamicClient(k8s_client), 'auth_key': kubeconfig.api_key, 'cluster_url': apihost}
        except Exception as e:
            logging.error('Failed to initialize Kubernetes and OpenShift client: {0}'.format(str(e)))
            raise

    def get_dyn_client_list(self):
        listofurl = get_cluster_url(self.var_file_content, self.dc, self.env)
        dynamiclient_list = []
        for url in listofurl:
            tmpdynamic = self.get_client(url)
            dynamiclient_list.append(tmpdynamic)
        print(f'get_dyn_client_list {dynamiclient_list}')
        return dynamiclient_list
        #list of dict containing oclient ,authkey and clusterurl


# obj = OCClient('N1DC','Production')
# obj.get_client('https://api.n1okd-pclus03.india.airtel.itm:6443')


def get_dyn_oc_client(cluster_api):
    """
        Returns a dynamic OpenShift client for the given cluster API.

        Args:
        - cluster_api: A string representing the API URL of the OpenShift cluster.

        Returns:
        - An OpenShift client object if authentication succeeds, otherwise 0.
        """
    occlnt_obj = OCClient('', '')
    oc_dyn_client_dict = occlnt_obj.get_client(cluster_api)
    if oc_dyn_client_dict['auth_key'] != 0:
        oc_dyn_client = oc_dyn_client_dict['dclient']
    else:
        oc_dyn_client = 0
    return oc_dyn_client