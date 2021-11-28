#
# modules/db_blockstorage.py
#

import os
import sqlite3

class DbBlockStorage():
    def __init__(self, db_dir):
        blockstorage_db_table = '''
            CREATE TABLE IF NOT EXISTS blockstorage (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                ad TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                size_gbs INTEGER NOT NULL,
                size_mbs INTEGER NOT NULL,
                vpus_per_gb INTEGER NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''

        blockstorage_db_file = db_dir + '/blockstorage.db'        
        
        if not os.path.isfile(blockstorage_db_file):            
            self._db = sqlite3.connect(blockstorage_db_file)
            self._db.execute(blockstorage_db_table)
        else:
            self._db = sqlite3.connect(blockstorage_db_file)

    def add(self, blockstorage_dict):        
        dml = '''
           INSERT INTO blockstorage (region, compartment_id, name, ad, lifecycle_state, 
              size_gbs, size_mbs, vpus_per_gb, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%d", "%d", "%d", "%s", "%s", "%s");
        ''' % (blockstorage_dict['region'], blockstorage_dict['compartment_id'], 
        blockstorage_dict['name'], blockstorage_dict['ad'], blockstorage_dict['lifecycle_state'],
        blockstorage_dict['size_gbs'], blockstorage_dict['size_mbs'], blockstorage_dict['vpus_per_gb'],
        blockstorage_dict['ocid'], blockstorage_dict['owner'], blockstorage_dict['created_on'],)

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()