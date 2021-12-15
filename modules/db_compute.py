#
# modules/db_compute.py
#

import os
import sqlite3

class DbCompute():
    def __init__(self, db_dir):
        compute_db_table = [
            '''
                CREATE TABLE IF NOT EXISTS compute (
                   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   region TEXT NOT NULL,
                   compartment_id TEXT NOT NULL,
                   name TEXT NOT NULL,
                   ad TEXT NOT NULL,
                   lifecycle_state TEXT NOT NULL,
                   shape TEXT NOT NULL,
                   ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                   owner TEXT NOT NULL,
                   created_on TEXT NOT NULL
                );
           ''',
           '''
                CREATE TABLE IF NOT EXISTS custom_img (
                   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   region TEXT NOT NULL,
                   compartment_id TEXT NOT NULL,
                   name TEXT NOT NULL,
                   ocid TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                   billable_size_in_gbs INTEGER NOT NULL,
                   operating_system TEXT NOT NULL,
                   operating_system_version TEXT NOT NULL,
                   size_in_mbs INTEGER NOT NULL,
                   owner TEXT NOT NULL,
                   created_on TEXT NOT NULL
                );
           '''
        ]
       
        compute_db_file = db_dir + '/compute.db'        
        
        if not os.path.isfile(compute_db_file):
            self._conn = sqlite3.connect(compute_db_file)
            self._cursor = self._conn.cursor()

            for table in compute_db_table:                
                self._cursor.execute(table)
        else:
            self._conn = sqlite3.connect(compute_db_file)
            self._cursor = self._conn.cursor()

    def add_compute(self, compute_dict):        
        dml = '''
           INSERT INTO compute (region, compartment_id, name, ad, lifecycle_state, 
              shape, ocid, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");
        ''' % (compute_dict['region'], compute_dict['compartment_id'], compute_dict['name'],
        compute_dict['ad'], compute_dict['lifecycle_state'], compute_dict['shape'],
        compute_dict['ocid'], compute_dict['owner'], compute_dict['created_on'],)       

        self._cursor.execute(dml)
        self._conn.commit()

        return self._cursor.lastrowid
    
    def add_custom_image(self, custom_img_dict):        
        dml = '''
           INSERT INTO custom_img (region, compartment_id, name, ocid, billable_size_in_gbs, 
              operating_system, operating_system_version, size_in_mbs, owner, created_on) 
           VALUES ("%s", "%s", "%s", "%s", "%d", "%s", "%s", "%d", "%s", "%s");
        ''' % (custom_img_dict['region'], custom_img_dict['compartment_id'], custom_img_dict['name'],
        custom_img_dict['ocid'], custom_img_dict['billable_size_in_gbs'], custom_img_dict['operating_system'],
        custom_img_dict['operating_system_version'], custom_img_dict['size_in_mbs'], custom_img_dict['owner'], 
        custom_img_dict['created_on'],)       

        self._cursor.execute(dml)
        self._conn.commit()

        return self._cursor.lastrowid
    
    def delete_compute(self, id):
        dml = '''
            DELETE FROM compute WHERE id = %d;
        ''' % (id,)

        self._cursor.execute(dml)
        self._conn.commit()
    
    def delete_custom_image(self, id):
        dml = '''
            DELETE FROM custom_img WHERE id = %d;
        ''' % (id,)

        self._cursor.execute(dml)
        self._conn.commit()
        
    def list_computes(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT id, region, ocid, owner FROM compute WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, owner FROM compute;
            '''

        self._cursor.execute(dml)
        computes_list = self._cursor.fetchall()

        return computes_list
    
    def list_custom_images(self, owner=None):
        if owner is not None:
            dml = '''
               SELECT id, region, ocid, owner FROM custom_img WHERE owner LIKE "%%%s";
            ''' % (owner,)            
        else:
            dml = '''
               SELECT id, region, ocid, owner FROM custom_img;
            '''

        self._cursor.execute(dml)
        custom_imgs_list = self._cursor.fetchall()

        return custom_imgs_list

    def close(self):
         self._conn.close()