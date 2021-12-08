#
# modules/db_fss.py
#

import os
import sqlite3

class DbFss():
    def __init__(self, db_dir):        
        fss_db_table = '''
            CREATE TABLE IF NOT EXISTS fss (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                ad TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''
        
        fss_db_file = db_dir + '/fss.db'        
        
        if not os.path.isfile(fss_db_file):            
            self._db = sqlite3.connect(fss_db_file)
            self._db.execute(fss_db_table)
        else:
            self._db = sqlite3.connect(fss_db_file)

    def add(self, fss_dict):        
        dml = '''
           INSERT INTO fss (region, compartment_id, name, ad, lifecycle_state, 
               ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (fss_dict['region'], fss_dict['compartment_id'], fss_dict['name'],        
        fss_dict['ad'], fss_dict['lifecycle_state'], fss_dict['ocid'], 
        fss_dict['owner'], fss_dict['created_on'],)       

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()
