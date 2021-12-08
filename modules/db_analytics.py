#
# modules/db_adb.py
#

import os
import sqlite3

class DbAnalytics():
    def __init__(self, db_dir):
        analytics_db_table = '''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                capacity_type TEXT NOT NULL,
                capacity_value INTEGER NOT NULL,
                feature_set TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                license_type TEXT NOT NULL,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''
        
        analytics_db_file = db_dir + '/analytics.db'        
        
        if not os.path.isfile(analytics_db_file):            
            self._db = sqlite3.connect(analytics_db_file)
            self._db.execute(analytics_db_table)
        else:
            self._db = sqlite3.connect(analytics_db_file)

    def add(self, analytics_dict):
        dml = '''
           INSERT INTO analytics (region, compartment_id, name, capacity_type, capacity_value, 
              feature_set, lifecycle_state, ocid, license_type, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (analytics_dict['region'], analytics_dict['compartment_id'], analytics_dict['name'],
        analytics_dict['capacity_type'], analytics_dict['capacity_value'], analytics_dict['feature_set'],
        analytics_dict['lifecycle_state'],  analytics_dict['ocid'], analytics_dict['license_type'], 
        analytics_dict['owner'], analytics_dict['created_on'],)

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()
