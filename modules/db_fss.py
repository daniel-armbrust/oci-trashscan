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
             CREATE TABLE IF NOT EXISTS fss_export (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                region TEXT NOT NULL,
                compartment_id TEXT NOT NULL,
                export_set_id TEXT NOT NULL,
                file_system_id TEXT NOT NULL,
                ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE
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
                subnet_id TEXT NOT NULL
            );
            '''
        ]    

        fss_db_file = db_dir + '/fss.db'        
        
        if not os.path.isfile(fss_db_file):            
            self._db = sqlite3.connect(fss_db_file)
            
            for table in fss_db_table:
                self._db.execute(table)
        else:
            self._db = sqlite3.connect(fss_db_file)

    def add_filesystem(self, fss_fs_dict):        
        dml = '''
           INSERT INTO fss_filesystem (region, compartment_id, name, ad, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (fss_fs_dict['region'], fss_fs_dict['compartment_id'], fss_fs_dict['name'],        
        fss_fs_dict['ad'], fss_fs_dict['ocid'], fss_fs_dict['owner'], fss_fs_dict['created_on'],)       

        self._db.execute(dml)
        self._db.commit()
    
    def add_export(self, fss_exp_dict):        
        dml = '''
           INSERT INTO fss_export (region, compartment_id, export_set_id, file_system_id, ocid) 
           VALUES ("%s", "%s", "%s", "%s", "%s");
        ''' % (fss_exp_dict['region'], fss_exp_dict['compartment_id'], fss_exp_dict['export_set_id'],        
        fss_exp_dict['file_system_id'], fss_exp_dict['ocid'],)       

        self._db.execute(dml)
        self._db.commit()
    
    def add_mounttarget(self, fss_mt_dict):        
        dml = '''
           INSERT INTO fss_mounttarget (region, compartment_id, name, ad, ocid, subnet_id) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (fss_mt_dict['region'], fss_mt_dict['compartment_id'], fss_mt_dict['name'],        
        fss_mt_dict['ad'], fss_mt_dict['ocid'], fss_mt_dict['subnet_id'],)       

        self._db.execute(dml)
        self._db.commit()
    
    def list_filesystem(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT id, region, ocid, owner FROM fss_filesystem WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, owner FROM fss_filesystem;
            '''

        cursor = self._db.execute(dml)
        filesystem_list = cursor.fetchall()

        return filesystem_list
    
    def list_export(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT id, region, ocid, owner FROM fss_export WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, owner FROM fss_export;
            '''

        cursor = self._db.execute(dml)
        export_list = cursor.fetchall()

        return export_list
    
    def list_mounttarget(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT id, region, ocid, owner FROM fss_mounttarget WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, owner FROM fss_mounttarget;
            '''

        cursor = self._db.execute(dml)
        mounttarget_list = cursor.fetchall()

        return mounttarget_list
    
    def delete_filesystem(self, id):
        dml = '''
            DELETE FROM fss_filesystem WHERE id = %d;
        ''' % (id,)

        self._db.execute(dml)
        self._db.commit()
    
    def delete_mounttarget(self, id):
        dml = '''
            DELETE FROM fss_mounttarget WHERE id = %d;
        ''' % (id,)

        self._db.execute(dml)
        self._db.commit()
    
    def delete_export(self, id):
        dml = '''
            DELETE FROM fss_export WHERE id = %d;
        ''' % (id,)

        self._db.execute(dml)
        self._db.commit()

    def close(self):
        self._db.close()   
