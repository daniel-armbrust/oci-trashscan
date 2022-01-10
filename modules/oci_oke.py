#
# modules/oci_oke.py
#

from time import sleep

from oci.container_engine import ContainerEngineClient
from oci import retry as oci_retry


class OciOke():
    def __init__(self, oci_config, timeout=120):
        self.__okeclient = ContainerEngineClient(oci_config, timeout=timeout)
    
    def list_clusters(self, compartment_id):
        """Lists all OKE (Oracle Kubernetes Engine) in a compartment.

        """
        cluster_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETING', 'DELETED',)        
        
        while True:
            resp = self.__okeclient.list_clusters(compartment_id=compartment_id, 
                page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    cluster_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break
          
        return cluster_list
        