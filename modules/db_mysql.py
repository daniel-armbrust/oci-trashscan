#
# modules/db_mysql.py
#

import os
import sqlite3

class DbMysql():
    def __init__(self, db_dir):        
        adb_db_table = '''
            CREATE TABLE IF NOT EXISTS mysql (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                version TEXT NOT NULL,
                shape TEXT NOT NULL,
                highly_available TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''
        
        odb_db_file = db_dir + '/mysql.db'        
        
        if not os.path.isfile(odb_db_file):            
            self._db = sqlite3.connect(odb_db_file)
            self._db.execute(adb_db_table)
        else:
            self._db = sqlite3.connect(odb_db_file)

    def add(self, mysql_dict):        
        dml = '''
           INSERT INTO mysql (region, compartment_id, name, version, shape, 
              highly_available, lifecycle_state, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (mysql_dict['region'], mysql_dict['compartment_id'], mysql_dict['name'],
        mysql_dict['version'], mysql_dict['shape'], mysql_dict['highly_available'],
        mysql_dict['lifecycle_state'], mysql_dict['ocid'], mysql_dict['owner'], 
        mysql_dict['created_on'],)       

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()
