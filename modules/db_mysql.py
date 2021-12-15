#
# modules/db_mysql.py
#

import os
import sqlite3

class DbMysql():
    def __init__(self, db_dir):        
        mysql_db_table = '''
            CREATE TABLE IF NOT EXISTS mysql (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                version TEXT NOT NULL,
                shape TEXT NOT NULL,
                highly_available TEXT NOT NULL,                
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''
        
        mysql_db_file = db_dir + '/mysql.db'        
        
        if not os.path.isfile(mysql_db_file):
            self._conn = sqlite3.connect(mysql_db_file)
            self._cursor = self._conn.cursor()
            self._cursor.execute(mysql_db_table)                
        else:
            self._conn = sqlite3.connect(mysql_db_file)
            self._cursor = self._conn.cursor()

    def add(self, mysql_dict):        
        dml = '''
           INSERT INTO mysql (region, compartment_id, name, version, shape, 
              highly_available, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (mysql_dict['region'], mysql_dict['compartment_id'], mysql_dict['name'],
        mysql_dict['version'], mysql_dict['shape'], mysql_dict['highly_available'],
        mysql_dict['ocid'], mysql_dict['owner'], mysql_dict['created_on'],)       

        self._cursor.execute(dml)
        self._conn.commit()

        return self._cursor.lastrowid
    
    def list(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT id, region, ocid, owner FROM mysql WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, owner FROM mysql;
            '''

        self._cursor.execute(dml)
        mysql_list = self._cursor.fetchall()

        return mysql_list
    
    def delete(self, id):
        dml = '''
            DELETE FROM mysql WHERE id = %d;
        ''' % (id,)

        self._cursor.execute(dml)
        self._conn.commit()

    def close(self):
        self._conn.close()
