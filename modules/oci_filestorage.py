#
# modules/oci_filestorage.py
#

from time import sleep

from oci.file_storage import FileStorageClient
from oci import retry as oci_retry
from oci.exceptions import ServiceError


class OciFileStorage():
    def __init__(self, oci_config, timeout=120):
        self._fssclient = FileStorageClient(oci_config, timeout=timeout)
    
    def list_filesystems(self, compartment_id, ad):
        """List all File Storage file systems in the specified compartment.
        
        """
        filesystem_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETING', 'DELETED',)        

        while True:
            resp = self._fssclient.list_file_systems(compartment_id=compartment_id, 
                availability_domain=ad, page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    filesystem_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

        return filesystem_list
    
    def list_exports(self, compartment_id):
        """List all export resources in the specified compartment.
        
        """
        exports_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETING', 'DELETED',)        

        while True:
            resp = self._fssclient.list_exports(compartment_id=compartment_id, 
                page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                resp_data.compartment_id = compartment_id

                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    exports_list.append(resp_data)
                                        
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

        return exports_list
    
    def list_mounttargets(self, compartment_id, ad):
        """List all mount target resources in the specified compartment.
        
        """
        mt_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETING', 'DELETED',)        

        while True:
            resp = self._fssclient.list_mount_targets(compartment_id=compartment_id, 
                availability_domain=ad, page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    mt_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

        return mt_list
    
    def list_snapshots(self, filesystem_id):
        """Lists snapshots of the specified file system.
        
        """
        snapshot_list = []
        next_page_id = None
        invalid_lifecycle_state = ('DELETING', 'DELETED',)        

        while True:
            resp = self._fssclient.list_snapshots(file_system_id=filesystem_id, 
                page=next_page_id, retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
           
            for resp_data in resp.data:
                if resp_data.lifecycle_state not in invalid_lifecycle_state:
                    snapshot_list.append(resp_data)
                            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

        return snapshot_list
    
    def exists_filesystem(self, ocid):
        """Check if the specified filesystem exists.

        """
        invalid_lifecycle_state = ('DELETING', 'DELETED',)
        
        try:
            resp = self._fssclient.get_file_system(file_system_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
        
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False
    
    def exists_snapshot(self, ocid):
        """Check if the specified snapshot exists.

        """
        invalid_lifecycle_state = ('DELETING', 'DELETED',)
        
        try:
            resp = self._fssclient.get_snapshot(snapshot_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
        
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False
    
    def exists_mounttarget(self, ocid):
        """Check if the specified filesystem exists.

        """
        invalid_lifecycle_state = ('DELETING', 'DELETED',)
        
        try:
            resp = self._fssclient.get_mount_target(mount_target_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
        
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False

    def exists_export(self, ocid):
        """Check if the specified export exists.

        """
        invalid_lifecycle_state = ('DELETING', 'DELETED',)
        
        try:
            resp = self._fssclient.get_export(export_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
        
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False
    
    def delete_filesystem(self, ocid):
        """Delete the specified filesystem.

        """
        resp = self._fssclient.delete_file_system(file_system_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False
    
    def delete_snapshot(self, ocid):
        """Delete the specified snapshot.

        """
        resp = self._fssclient.delete_snapshot(snapshot_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False
    
    def delete_mounttarget(self, ocid):
        """Delete the specified mount target.

        """
        resp = self._fssclient.delete_mount_target(mount_target_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False

    def delete_export(self, ocid):
        """Delete the specified mount target.

        """
        resp = self._fssclient.delete_export(export_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False
        
    
