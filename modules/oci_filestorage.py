#
# modules/oci_filestorage.py
#

from time import sleep

from oci.file_storage import FileStorageClient
from oci import retry as oci_retry


class OciFileStorage():
    def __init__(self, oci_config, timeout=120):
        self._fssclient = FileStorageClient(oci_config, timeout=timeout)
    
    def list_filesystems(self, compartment_id, ad, sleep_time=0):
        """List all File Storage file systems in the specified compartment.
        
        """
        filesystem_list = []
        next_page_id = None

        while True:
            resp = self._fssclient.list_file_systems(compartment_id=compartment_id, 
                availability_domain=ad, page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                filesystem_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return filesystem_list