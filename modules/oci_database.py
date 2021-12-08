#
# modules/oci_database.py
#

from time import sleep

from oci import database
from oci import mysql
from oci import retry as oci_retry


class OciDatabase():
    def __init__(self, oci_config, timeout=120): 
        self._oci_config = oci_config
        self._timeout = timeout      
      
    def list_adb(self, compartment_id, sleep_time=0):
        """List all Autonomous Databases from the specified compartment.

        """
        adb_list = []
        next_page_id = None

        dbclient = database.DatabaseClient(self._oci_config, timeout=self._timeout)

        while True:
            resp = dbclient.list_autonomous_databases(compartment_id, page=next_page_id,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)          
           
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
        next_page_id = None

        dbclient = database.DatabaseClient(self._oci_config, timeout=self._timeout)
        
        while True:
            resp = dbclient.list_db_systems(compartment_id, page=next_page_id)          
           
            for resp_data in resp.data:
                odb_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return odb_list
    
    def list_mysql(self, compartment_id, sleep_time=0):
        """List all MySQL DB Systems in the specified compartment.
        
        """
        mysql_list = []
        next_page_id = None

        dbclient = mysql.DbSystemClient(self._oci_config, timeout=self._timeout)

        while True:
            resp = dbclient.list_db_systems(compartment_id, page=next_page_id)          
           
            for resp_data in resp.data:
                mysql_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break

            # Wait for the next API query to not flood the OCI
            sleep(sleep_time)

        return mysql_list

    def get_mysql(self, mysql_id):
        """Get information about the specified MySQL DB System.

        """
        dbclient = mysql.DbSystemClient(self._oci_config, timeout=self._timeout)

        resp_data = dbclient.get_db_system(mysql_id).data

        return resp_data

