#
# modules/db_odb.py
#

import os
import sqlite3

class DbOdb():
    def __init__(self, db_dir):        
        odb_db_table = '''
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
            self._conn = sqlite3.connect(odb_db_file)
            self._cursor = self._conn.cursor()
            self._cursor.execute(odb_db_table)                    
        else:
            self._conn = sqlite3.connect(odb_db_file)
            self._cursor = self._conn.cursor()

    def add(self, adb_dict):        
        dml = '''
           INSERT INTO odb (region, compartment_id, name, edition, shape, 
              storage_gbs, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s");
        ''' % (adb_dict['region'], adb_dict['compartment_id'], adb_dict['name'],
        adb_dict['edition'], adb_dict['shape'], adb_dict['storage_gbs'],
        adb_dict['ocid'], adb_dict['owner'], adb_dict['created_on'],)       

        self._cursor.execute(dml)
        self._conn.commit()

        return self._cursor.lastrowid

    def delete(self, id):
        dml = '''
            DELETE FROM odb WHERE id = %d;
        ''' % (id,)

        self._cursor.execute(dml)
        self._conn.commit()

    def list(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT id, region, ocid, owner FROM odb WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, owner FROM odb;
            '''

        self._cursor.execute(dml)
        odb_list = self._cursor.fetchall()

        return odb_list

    def close(self):
        self._db.close()
