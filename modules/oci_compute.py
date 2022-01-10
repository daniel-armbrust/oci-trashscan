#
# modules/oci_compute.py
#

from time import sleep

from oci.core import ComputeClient
from oci.exceptions import ServiceError
from oci import retry as oci_retry


class OciCompute():
    def __init__(self, oci_config, timeout=120):
        self.__cptclient = ComputeClient(oci_config, timeout=timeout)
    
    def list_computes(self, compartment_id):
        """List all the compute instances in the specified compartment.
        
        """
        compute_list = []
        next_page_id = None
        invalid_lifecycle_state = ('TERMINATING', 'TERMINATED',)        

        while True:
            resp = self.__cptclient.list_instances(compartment_id=compartment_id, page=next_page_id,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)          
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    compute_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break
           
        return compute_list
    
    def list_custom_images(self, compartment_id):
        """List all custom images available in the specified compartment.

        """
        images_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETED',)

        while True:
            resp = self.__cptclient.list_images(compartment_id=compartment_id, page=next_page_id,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)          
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    if not type(resp_data.base_image_id) == None.__class__:            
                        images_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break
           
        return images_list

    def exists_compute(self, ocid):
        """Check if the compute exists.
        
        """
        invalid_lifecycle_state = ('TERMINATING', 'TERMINATED',)

        try:
            resp = self.__cptclient.get_instance(instance_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
                
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False
    
    def exists_custom_image(self, ocid):
        """Check if the custom image exists.
        
        """
        invalid_lifecycle_state = ('DELETED',)

        try:
            resp = self.__cptclient.get_image(image_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
                
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False

    def delete_custom_image(self, ocid):
        """Delete the specified Custom Image.

        """
        resp = self.__cptclient.delete_image(image_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False

    def terminate(self, ocid):
        """Terminates the specified instance.

        """        
        resp = self.__cptclient.terminate_instance(instance_id=ocid, 
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)                               

        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False        