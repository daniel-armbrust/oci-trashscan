#
# modules/oci_database.py
#

from time import sleep

from oci import database
from oci import mysql
from oci import retry as oci_retry
from oci.exceptions import ServiceError


class OciDatabase():
    def __init__(self, oci_config, timeout=120): 
        self._oci_config = oci_config
        self._timeout = timeout      
      
    def list_adb(self, compartment_id):
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

        return adb_list

    def exists_adb(self, ocid):
        """Check if the Autonomous Database exists.
        
        """        
        invalid_lifecycle_state = ('TERMINATING', 'TERMINATED',)

        dbclient = database.DatabaseClient(self._oci_config, timeout=self._timeout)        

        try:
            resp = dbclient.get_autonomous_database(autonomous_database_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
                
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False

    def delete_adb(self, ocid):
        """Delete the specified Autonomous Database.
        
        """
        dbclient = database.DatabaseClient(self._oci_config, timeout=self._timeout)        

        resp = dbclient.delete_autonomous_database(autonomous_database_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
              
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False                

    def list_odb(self, compartment_id):
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
            
        return odb_list
    
    def exists_odb(self, ocid):
        """Check if the Oracle Database exists.
        
        """
        invalid_lifecycle_state = ('DELETING', 'DELETED',)

        dbclient = database.DatabaseClient(self._oci_config, timeout=self._timeout)        

        try:
            resp = dbclient.get_db_system(db_system_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
                
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False
    
    def delete_odb(self, ocid):
        """Delete the specified Oracle Database.

        """
        dbclient = database.DatabaseClient(self._oci_config, timeout=self._timeout)        

        resp = dbclient.delete_database(database_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False                

    def list_mysql(self, compartment_id):
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
            
        return mysql_list

    def exists_mysql(self, ocid):
        """Check if the MySQL Database exists.

        """
        invalid_lifecycle_state = ('DELETING', 'DELETED',)

        dbclient = mysql.DbSystemClient(self._oci_config, timeout=self._timeout)    
        
        try:
            resp = dbclient.get_db_system(db_system_id=ocid,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        except ServiceError:
            return False
                
        lifecycle_state = resp.data.lifecycle_state
        
        if lifecycle_state not in invalid_lifecycle_state:
            return True
        else:
            return False
    
    def delete_mysql(self, ocid):
        """Delete the specified MySQL DB System.

        """
        dbclient = mysql.DbSystemClient(self._oci_config, timeout=self._timeout)    

        resp = dbclient.delete_db_system(db_system_id=ocid,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)
        
        if resp.status >= 200 and resp.status < 300:
            return True
        else:
            return False                

    def get_mysql(self, ocid):
        """Get information about the specified MySQL DB System.

        """
        dbclient = mysql.DbSystemClient(self._oci_config, timeout=self._timeout)

        resp_data = dbclient.get_db_system(db_system_id=ocid).data

        return resp_data