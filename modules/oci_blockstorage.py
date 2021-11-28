#
# modules/oci_blockvolume.py
#

from time import sleep

from oci.core import BlockstorageClient


class OciBlockStorage():
    def __init__(self, oci_config):
        self._blkstrclient = BlockstorageClient(oci_config)
    
    def list_volumes(self, compartment_id, sleep_time=0):
        """Lists all the block volumes in the specified compartment.

        """
        blkvol_list = []
        next_page_id = ''
        
        while True:
            resp = self._blkstrclient.list_volumes(compartment_id, page=next_page_id)
           
            for resp_data in resp.data:
                blkvol_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return blkvol_list
        