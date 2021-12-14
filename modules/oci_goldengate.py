#
# modules/oci_goldengate.py
#

from time import sleep

from oci.golden_gate import GoldenGateClient
from oci import retry as oci_retry


class OciGoldenGate():
    def __init__(self, oci_config, timeout=120):
        self._ggclient = GoldenGateClient(oci_config, timeout=timeout)
    
    def list_database_registrations(self, compartment_id):
        """Lists all the DatabaseRegistrations in the compartment.
        
        """
        dbr_list = []
        next_page_id = None
     
        while True:
            resp = self._ggclient.list_database_registrations(compartment_id=compartment_id, 
                page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)          
           
            for resp_data in resp.data:
                dbr_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break
        
        return dbr_list