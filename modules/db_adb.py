#
# modules/db_adb.py
#

import os
import sqlite3

class DbAdb():
    def __init__(self, db_dir):
        adb_db_table = '''
            CREATE TABLE IF NOT EXISTS adb (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                ocpu INTEGER NOT NULL,
                storage_gbs INTEGER NOT NULL,
                storage_tbs INTEGER NOT NULL,
                workload_type TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''
        
        adb_db_file = db_dir + '/adb.db'        
        
        if not os.path.isfile(adb_db_file):            
            self._db = sqlite3.connect(adb_db_file)
            self._db.execute(adb_db_table)
        else:
            self._db = sqlite3.connect(adb_db_file)

    def add(self, adb_dict):
        dml = '''
           INSERT INTO adb (region, compartment_id, name, ocpu, storage_gbs, 
              storage_tbs, workload_type, lifecycle_state, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%d", "%d", "%d", "%s", "%s", "%s", "%s", "%s");
        ''' % (adb_dict['region'], adb_dict['compartment_id'], adb_dict['name'],
        adb_dict['ocpu'], adb_dict['storage_gbs'], adb_dict['storage_tbs'],
        adb_dict['workload_type'],  adb_dict['lifecycle_state'], adb_dict['ocid'], 
        adb_dict['owner'], adb_dict['created_on'],)

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()
