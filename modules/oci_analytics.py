#
# modules/oci_analytics.py
#

from time import sleep

from oci.analytics import AnalyticsClient
from oci import retry as oci_retry


class OciAnalytics():
    def __init__(self, oci_config, timeout=120):
        self._alytsclient = AnalyticsClient(oci_config, timeout=timeout)
    
    def list_instances(self, compartment_id, sleep_time=0):
        """Lists all Analytics instances in a compartment.

        """
        analytics_list = []
        next_page_id = None
        
        while True:
            resp = self._alytsclient.list_analytics_instances(compartment_id=compartment_id, 
                page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                analytics_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return analytics_list
        