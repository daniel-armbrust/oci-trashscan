#
# modules/oci_analytics.py
#

from time import sleep

from oci.analytics import AnalyticsClient
from oci import retry as oci_retry
from oci.exceptions import ServiceError


class OciAnalytics():
    def __init__(self, oci_config, timeout=120):
        self._alytsclient = AnalyticsClient(oci_config, timeout=timeout)
    
    def list_instances(self, compartment_id):
        """Lists all Analytics instances in a compartment.

        """
        analytics_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETING', 'DELETED',)
        
        while True:
            resp = self._alytsclient.list_analytics_instances(compartment_id=compartment_id, 
                page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    analytics_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

        return analytics_list

    def exists(self, ocid):
        """Check if the Analytics instances exists.
        
        """
        invalid_lifecycle_state = ('DELETING', 'DELETED',)

        try:
            resp = self.self._alytsclient(analytics_instance_id=ocid,            
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
                
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False    
    
    def delete(self, ocid):
        """Deletes the specified Analytics instances.

        """        
        resp = self._alytsclient.delete_analytics_instance(analytics_instance_id=ocid, 
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)                
               
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False        