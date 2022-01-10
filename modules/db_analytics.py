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
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                license_type TEXT NOT NULL,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''
        
        analytics_db_file = db_dir + '/analytics.db'        
        
        if not os.path.isfile(analytics_db_file):
            self.__conn = sqlite3.connect(analytics_db_file)
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(analytics_db_table)
        else:
            self.__conn = sqlite3.connect(analytics_db_file)
            self.__cursor = self.__conn.cursor()

    def add(self, analytics_dict):
        dml = '''
           INSERT INTO analytics (region, compartment_id, name, capacity_type, capacity_value, 
              feature_set, ocid, license_type, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (analytics_dict['region'], analytics_dict['compartment_id'], analytics_dict['name'],
        analytics_dict['capacity_type'], analytics_dict['capacity_value'], analytics_dict['feature_set'],
        analytics_dict['ocid'], analytics_dict['license_type'], analytics_dict['owner'], 
        analytics_dict['created_on'],)

        self.__cursor.execute(dml)
        self.__conn.commit()

        return self.__cursor.lastrowid

    def list(self, owner=None):
        if owner is not None:
            dml = '''              
               SELECT id, region, compartment_id, name, capacity_type, capacity_value, feature_set, 
                   ocid, license_type, owner, created_on
               FROM analytics WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, compartment_id, name, capacity_type, capacity_value, feature_set, 
                   ocid, license_type, owner, created_on
               FROM analytics;
            '''

        self.__cursor.execute(dml)
        analytics_list = self.__cursor.fetchall()

        return analytics_list

    def delete(self, id):
        dml = '''
            DELETE FROM analytics WHERE id = %d;
        ''' % (id,)

        self.__cursor.execute(dml)
        self.__conn.commit()

    def close(self):
        self.__conn.close()
