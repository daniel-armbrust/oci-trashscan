#
# modules/oci_blockvolume.py
#

from time import sleep

from oci.core import BlockstorageClient
from oci.core.models import UpdateVolumeDetails
from oci.exceptions import ServiceError
from oci import retry as oci_retry


class OciBlockStorage():
    def __init__(self, oci_config, timeout=120):
        self._blkstrclient = BlockstorageClient(oci_config, timeout=timeout)
    
    def list_volumes(self, compartment_id):
        """Lists all the block volumes in the specified compartment.

        """
        blkvol_list = []
        next_page_id = None
        invalid_lifecycle_state = ('TERMINATING', 'TERMINATED',)        
        
        while True:
            resp = self._blkstrclient.list_volumes(compartment_id, page=next_page_id,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    blkvol_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

        return blkvol_list
    
    def delete_replica(self, ocid):
        """Deletes the specified Block Volume Replica 

        """
        resp = self._blkstrclient.update_volume(volume_id=ocid, 
            update_volume_details=UpdateVolumeDetails(block_volume_replicas=[]),
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False        
    
    def delete_volume_group(self, ocid):
        """Deletes the specified Block Volume Group 

        """
        resp = self._blkstrclient.delete_volume_group(volume_group_id=ocid,             
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False        
        
    def delete_volume(self, ocid):
        """Deletes the specified Block Volume.

        """        
        resp = self._blkstrclient.delete_volume(volume_id=ocid, 
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)                
               
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False        
    
    def exists(self, ocid):
        """Check if the specified Block Volume exists.
        
        """
        invalid_lifecycle_state = ('TERMINATING', 'TERMINATED',)
        
        try:            
            resp = self._blkstrclient.get_volume(volume_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
        
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False