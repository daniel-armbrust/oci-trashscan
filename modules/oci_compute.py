#
# modules/oci_compute.py
#

from time import sleep

from oci.core import ComputeClient


class OciCompute():
    def __init__(self, oci_config):
        self._cptclient = ComputeClient(oci_config)
    
    def list_instances(self, compartment_id, sleep_time=0):
        """List all the compute instances in the specified compartment.
        
        """
        compute_list = []
        next_page_id = ''

        while True:
            resp = self._cptclient.list_instances(compartment_id, page=next_page_id)          
           
            for resp_data in resp.data:
                compute_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return compute_list