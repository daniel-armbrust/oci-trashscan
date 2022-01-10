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
                size_gbs INTEGER NOT NULL,
                size_mbs INTEGER NOT NULL,
                vpus_per_gb INTEGER NOT NULL,
                replica_id TEXT NOT NULL,
                replica_ad TEXT NOT NULL,
                volume_group_id TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
        '''

        blockstorage_db_file = db_dir + '/blockstorage.db'        
        
        if not os.path.isfile(blockstorage_db_file):
            self.__conn = sqlite3.connect(blockstorage_db_file)
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(blockstorage_db_table)          
        else:
            self.__conn = sqlite3.connect(blockstorage_db_file)
            self.__cursor = self.__conn.cursor()

    def add(self, blockstorage_dict):        
        dml = '''
           INSERT INTO blockstorage (region, compartment_id, name, ad, 
              size_gbs, size_mbs, vpus_per_gb, replica_id, replica_ad, volume_group_id,
              ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%d", "%d", "%d", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (blockstorage_dict['region'], blockstorage_dict['compartment_id'], 
        blockstorage_dict['name'], blockstorage_dict['ad'], blockstorage_dict['size_gbs'], 
        blockstorage_dict['size_mbs'], blockstorage_dict['vpus_per_gb'], blockstorage_dict['replica_id'], 
        blockstorage_dict['replica_ad'], blockstorage_dict['volume_group_id'], blockstorage_dict['ocid'], 
        blockstorage_dict['owner'], blockstorage_dict['created_on'],)

        self.__cursor.execute(dml)
        self.__conn.commit()

        return self.__cursor.lastrowid

    def delete(self, id):
        dml = '''
            DELETE FROM blockstorage WHERE id = %d;
        ''' % (id,)

        self.__cursor.execute(dml)
        self.__conn.commit()

    def list(self, owner=None):
        if owner is not None:
            dml = '''              
               SELECT id, region, compartment_id, name, ad, size_gbs, size_mbs, vpus_per_gb, 
                 replica_id, replica_ad, volume_group_id, ocid, owner, created_on
               FROM blockstorage WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, compartment_id, name, ad, size_gbs, size_mbs, vpus_per_gb, 
                 replica_id, replica_ad, volume_group_id, ocid, owner, created_on
               FROM blockstorage;
            '''
        self.__cursor.execute(dml)
        blockstorages_list = self.__cursor.fetchall()

        return blockstorages_list

    def close(self):
        self.__conn.close()
    
