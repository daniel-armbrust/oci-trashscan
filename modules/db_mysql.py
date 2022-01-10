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
            self.__conn = sqlite3.connect(mysql_db_file)
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(mysql_db_table)                
        else:
            self.__conn = sqlite3.connect(mysql_db_file)
            self.__cursor = self.__conn.cursor()

    def add(self, mysql_dict):        
        dml = '''
           INSERT INTO mysql (region, compartment_id, name, version, shape, 
              highly_available, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (mysql_dict['region'], mysql_dict['compartment_id'], mysql_dict['name'],
        mysql_dict['version'], mysql_dict['shape'], mysql_dict['highly_available'],
        mysql_dict['ocid'], mysql_dict['owner'], mysql_dict['created_on'],)       

        self.__cursor.execute(dml)
        self.__conn.commit()

        return self.__cursor.lastrowid
    
    def list(self, owner=None):
        if owner is not None:
            dml = '''              
               SELECT id, region, compartment_id, name, version, shape, highly_available, 
                   ocid, owner, created_on 
               FROM mysql WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, compartment_id, name, version, shape, highly_available, 
                   ocid, owner, created_on FROM mysql;
            '''

        self.__cursor.execute(dml)
        mysql_list = self.__cursor.fetchall()

        return mysql_list
    
    def delete(self, id):
        dml = '''
            DELETE FROM mysql WHERE id = %d;
        ''' % (id,)

        self.__cursor.execute(dml)
        self.__conn.commit()

    def close(self):
        self.__conn.close()
