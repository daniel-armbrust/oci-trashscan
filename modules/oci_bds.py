#
# modules/oci_bds.py
#

from time import sleep

from oci.bds import BdsClient
from oci import retry as oci_retry


class OciBlockStorage():
    def __init__(self, oci_config, timeout=120):
        self._bdsclient = BdsClient(oci_config, timeout=timeout)
    
    def list_bds(self, compartment_id, sleep_time=0):
        """Lists all Big Data Service clusters in a compartment.

        """
        bds_list = []
        next_page_id = None
        
        while True:
            resp = self._bdsclient.list_bds_instances(compartment_id, page=next_page_id, 
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                bds_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return bds_list
        