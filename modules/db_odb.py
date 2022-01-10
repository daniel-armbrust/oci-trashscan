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
            self.__conn = sqlite3.connect(odb_db_file)
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(odb_db_table)                    
        else:
            self.__conn = sqlite3.connect(odb_db_file)
            self.__cursor = self.__conn.cursor()

    def add(self, adb_dict):        
        dml = '''
           INSERT INTO odb (region, compartment_id, name, edition, shape, 
              storage_gbs, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s");
        ''' % (adb_dict['region'], adb_dict['compartment_id'], adb_dict['name'],
        adb_dict['edition'], adb_dict['shape'], adb_dict['storage_gbs'],
        adb_dict['ocid'], adb_dict['owner'], adb_dict['created_on'],)       

        self.__cursor.execute(dml)
        self.__conn.commit()

        return self.__cursor.lastrowid

    def delete(self, id):
        dml = '''
            DELETE FROM odb WHERE id = %d;
        ''' % (id,)

        self.__cursor.execute(dml)
        self.__conn.commit()

    def list(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT  id, region, compartment_id, name, edition, shape, 
                   storage_gbs, ocid, owner, created_on FROM odb WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT  id, region, compartment_id, name, edition, shape, 
                   storage_gbs, ocid, owner, created_on FROM odb
            '''

        self.__cursor.execute(dml)
        odbs_list = self.__cursor.fetchall()

        return odbs_list

    def close(self):
        self.__conn.close()
