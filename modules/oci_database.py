#
# modules/oci_database.py
#

from time import sleep

from oci import database


class OciDatabase():
    def __init__(self, oci_config):        
        self._dbclient = database.DatabaseClient(oci_config)
      
    def list_adb(self, compartment_id, sleep_time=0):
        """List all Autonomous Databases from the specified compartment.

        """
        adb_list = []
        next_page_id = ''

        while True:
            resp = self._dbclient.list_autonomous_databases(compartment_id, page=next_page_id)          
           
            for resp_data in resp.data:
                adb_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return adb_list
    
    def list_odb(self, compartment_id, sleep_time=0):
        """List all Oracle Databases from the specified compartment.

        """
        odb_list = []
        next_page_id = ''
        
        while True:
            resp = self._dbclient.list_db_systems(compartment_id, page=next_page_id)          
           
            for resp_data in resp.data:
                odb_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return odb_list