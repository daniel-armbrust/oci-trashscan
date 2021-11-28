#
# modules/db_odb.py
#

import os
import sqlite3

class DbOdb():
    def __init__(self, db_dir):        
        adb_db_table = '''
            CREATE TABLE IF NOT EXISTS odb (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                edition TEXT NOT NULL,
                shape TEXT NOT NULL,
                storage_gbs INTEGER NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''
        
        odb_db_file = db_dir + '/odb.db'        
        
        if not os.path.isfile(odb_db_file):            
            self._db = sqlite3.connect(odb_db_file)
            self._db.execute(adb_db_table)
        else:
            self._db = sqlite3.connect(odb_db_file)

    def add(self, adb_dict):        
        dml = '''
           INSERT INTO odb (region, compartment_id, name, edition, shape, 
              storage_gbs, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s");
        ''' % (adb_dict['region'], adb_dict['compartment_id'], adb_dict['name'],
        adb_dict['edition'], adb_dict['shape'], adb_dict['storage_gbs'],
        adb_dict['ocid'], adb_dict['owner'], adb_dict['created_on'],)       

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()
