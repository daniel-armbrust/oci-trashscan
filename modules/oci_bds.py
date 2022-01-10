#
# modules/oci_bds.py
#

from time import sleep

from oci.bds import BdsClient
from oci import retry as oci_retry


class OciBigData():
    def __init__(self, oci_config, timeout=120):
        self.__bdsclient = BdsClient(oci_config, timeout=timeout)
    
    def list_bds(self, compartment_id):
        """Lists all Big Data Service clusters in a compartment.

        """
        bds_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETING', 'DELETED',)        
        
        while True:
            resp = self.__bdsclient.list_bds_instances(compartment_id, page=next_page_id, 
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    bds_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break            

        return bds_list
        