#
# modules/db_compute.py
#

import os
import sqlite3

class DbCompute():
    def __init__(self, db_dir):
        compute_db_table = '''
            CREATE TABLE IF NOT EXISTS compute (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                ad TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                shape TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''

        compute_db_file = db_dir + '/compute.db'        
        
        if not os.path.isfile(compute_db_file):            
            self._db = sqlite3.connect(compute_db_file)
            self._db.execute(compute_db_table)
        else:
            self._db = sqlite3.connect(compute_db_file)

    def add(self, compute_dict):        
        
        print(compute_dict)

        dml = '''
           INSERT INTO compute (region, compartment_id, name, ad, lifecycle_state, 
              shape, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (compute_dict['region'], compute_dict['compartment_id'], compute_dict['name'],
        compute_dict['ad'], compute_dict['lifecycle_state'], compute_dict['shape'],
        compute_dict['ocid'], compute_dict['owner'], compute_dict['created_on'],)       

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()