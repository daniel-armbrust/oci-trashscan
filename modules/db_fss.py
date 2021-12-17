#
# modules/db_fss.py
#

import os
import sqlite3

class DbFss():
    def __init__(self, db_dir):
        fss_db_table = [
            '''
            CREATE TABLE IF NOT EXISTS fss_filesystem (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                name TEXT NOT NULL,
                ad TEXT NOT NULL,                
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS fss_snapshot (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                name TEXT NOT NULL,                
                file_system_id TEXT NOT NULL,
                provenance_id TEXT NOT NULL,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL                
            );
            ''',          
            '''
             CREATE TABLE IF NOT EXISTS fss_mounttarget (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,                
                name TEXT NOT NULL,
                ad TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                subnet_id TEXT NOT NULL,
                owner TEXT NOT NULL,
                created_on TEXT NOT NULL                
            );
            '''
        ]    

        fss_db_file = db_dir + '/fss.db'        
        
        if not os.path.isfile(fss_db_file):
            self._conn = sqlite3.connect(fss_db_file)
            self._cursor = self._conn.cursor()
            
            for table in fss_db_table:                
                self._cursor.execute(table)
        else:
            self._conn = sqlite3.connect(fss_db_file)
            self._cursor = self._conn.cursor()

    def add_filesystem(self, fss_fs_dict):        
        dml = '''
           INSERT INTO fss_filesystem (region, compartment_id, name, ad, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (fss_fs_dict['region'], fss_fs_dict['compartment_id'], fss_fs_dict['name'],        
        fss_fs_dict['ad'], fss_fs_dict['ocid'], fss_fs_dict['owner'], fss_fs_dict['created_on'],)       

        self._cursor.execute(dml)
        self._conn.commit()

        return self._cursor.lastrowid
    
    def add_snapshot(self, fss_snp_dict):        
        dml = '''
           INSERT INTO fss_snapshot (region, ocid, name, owner, created_on, file_system_id, owner,
               provenance_id) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (fss_snp_dict['region'], fss_snp_dict['ocid'], fss_snp_dict['name'], fss_snp_dict['owner'],
        fss_snp_dict['created_on'], fss_snp_dict['file_system_id'], fss_snp_dict['owner'],
        fss_snp_dict['provenance_id'],)       

        self._cursor.execute(dml)
        self._conn.commit()

        return self._cursor.lastrowid
    
    def add_mounttarget(self, fss_mt_dict):        
        dml = '''
           INSERT INTO fss_mounttarget (region, compartment_id, name, ad, ocid, subnet_id,
               owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (fss_mt_dict['region'], fss_mt_dict['compartment_id'], fss_mt_dict['name'],        
        fss_mt_dict['ad'], fss_mt_dict['ocid'], fss_mt_dict['subnet_id'], fss_mt_dict['owner'],
        fss_mt_dict['created_on'],)       

        self._cursor.execute(dml)
        self._conn.commit()

        return self._cursor.lastrowid
    
    def list_filesystems(self, owner=None):
        if owner is not None:
            dml = '''             
               SELECT id, region, compartment_id, name, ad, ocid, owner, created_on 
               FROM fss_filesystem WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, compartment_id, name, ad, ocid, owner, created_on 
               FROM fss_filesystem;
            '''

        self._cursor.execute(dml)
        filesystems_list = self._cursor.fetchall()

        return filesystems_list
    
    def list_snapshots(self, owner=None):
        if owner is not None:
            dml = '''             
               SELECT id, region, ocid, name, file_system_id, provenance_id, owner, created_on
               FROM fss_snapshot WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, name, file_system_id, provenance_id, owner, created_on
               FROM fss_snapshot;
            '''

        self._cursor.execute(dml)
        snapshots_list = self._cursor.fetchall()

        return snapshots_list
       
    def list_mounttargets(self, owner=None):
        if owner is not None:
            dml = '''             
               SELECT id, region, compartment_id, name, ad, ocid, subnet_id, owner, 
                  created_on FROM fss_mounttarget WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, compartment_id, name, ad, ocid, subnet_id, owner, 
                  created_on FROM fss_mounttarget;
            '''

        self._cursor.execute(dml)
        mounttargets_list = self._cursor.fetchall()

        return mounttargets_list
    
    def delete_filesystem(self, id):
        dml = '''
            DELETE FROM fss_filesystem WHERE id = %d;
        ''' % (id,)
        
        self._cursor.execute(dml)
        self._conn.commit()
    
    def delete_snapshot(self, id):
        dml = '''
            DELETE FROM fss_snapshot WHERE id = %d;
        ''' % (id,)
        
        self._cursor.execute(dml)
        self._conn.commit()
    
    def delete_mounttarget(self, id):
        dml = '''
            DELETE FROM fss_mounttarget WHERE id = %d;
        ''' % (id,)

        self._cursor.execute(dml)
        self._conn.commit()
      
    def close(self):
        self._conn.close()   
