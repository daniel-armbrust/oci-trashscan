#
# modules/oci_compute.py
#

from time import sleep

from oci.core import ComputeClient
from oci.exceptions import ServiceError
from oci import retry as oci_retry


class OciCompute():
    def __init__(self, oci_config, timeout=120):
        self._cptclient = ComputeClient(oci_config, timeout=timeout)
    
    def list_instances(self, compartment_id):
        """List all the compute instances in the specified compartment.
        
        """
        compute_list = []
        next_page_id = None

        while True:
            resp = self._cptclient.list_instances(compartment_id, page=next_page_id,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)          
           
            for resp_data in resp.data:
                compute_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break
           
        return compute_list
    
    def exists(self, ocid):
        """Check if the compute exists.
        
        """
        invalid_lifecycle_state = ('TERMINATING', 'TERMINATED',)

        try:
            resp = self._cptclient.get_instance(instance_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
                
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False

    def terminate(self, ocid):
        """Terminates the specified instance.

        """        
        resp = self._cptclient.terminate_instance(instance_id=ocid, 
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)                               

        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False        