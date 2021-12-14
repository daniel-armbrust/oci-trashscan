#
# modules/oci_oke.py
#

from time import sleep

from oci.container_engine import ContainerEngineClient
from oci import retry as oci_retry


class OciOke():
    def __init__(self, oci_config, timeout=120):
        self._okeclient = ContainerEngineClient(oci_config, timeout=timeout)
    
    def list_clusters(self, compartment_id):
        """Lists all OKE (Oracle Kubernetes Engine) in a compartment.

        """
        cluster_list = []
        next_page_id = None
        
        while True:
            resp = self._okeclient.list_clusters(compartment_id=compartment_id, 
                page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                cluster_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break
          
        return cluster_list
        