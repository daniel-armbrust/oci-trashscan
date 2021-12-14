#
# modules/utils_delete.py
#

from . import oci_database
from . import oci_compute
from . import oci_blockstorage
from . import oci_filestorage

from . import db_adb
from . import db_odb
from . import db_compute
from . import db_blockstorage
from . import db_mysql
from . import db_fss
    

def adb(oci_config, db_dir, user_login_delete=None):
    """Delete Autonomous Databases.

    """
    db = db_adb.DbAdb(db_dir)

    adb_list = db.list(user_login_delete)

    for adb in adb_list:
        id = adb[0]
        region = adb[1]
        ocid = adb[2]
        owner = adb[3]

        print('--> Deleting AUTONOMOUS DATABASE (adb) - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_db = oci_database.OciDatabase(oci_config)
        exists = oci_db.exists_adb(ocid)

        if exists:
            deleted = oci_db.delete_adb(ocid)

            if deleted:
                db.delete(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete(id)
    
    db.close()


def odb(oci_config, db_dir, user_login_delete=None):
    """Delete Oracle Datbases.

    """
    db = db_adb.DbOdb(db_dir)

    odb_list = db.list(user_login_delete)

    for odb in odb_list:
        id = odb[0]
        region = odb[1]
        ocid = odb[2]
        owner = odb[3]

        print('--> Deleting ORACLE DATABASE (odb) - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_db = oci_database.OciDatabase(oci_config)
        exists = oci_db.exists_odb(ocid)

        if exists:
            deleted = oci_db.delete_odb(ocid)

            if deleted:
                db.delete(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete(id)
    
    db.close()


def compute(oci_config, db_dir, user_login_delete=None):
    """Delete Compute Instances.

    """
    db = db_compute.DbCompute(db_dir)

    compute_list = db.list(user_login_delete)

    for compute in compute_list:
        id = compute[0]
        region = compute[1]
        ocid = compute[2]
        owner = compute[3]

        print('--> Deleting COMPUTE INSTANCES - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_cpt = oci_compute.OciCompute(oci_config)
        exists = oci_cpt.exists(ocid)

        if exists:
            deleted = oci_cpt.terminate(ocid)

            if deleted:
                db.delete(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete(id)
    
    db.close()


def blockstorage(oci_config, db_dir, user_login_delete=None):
    """Delete Block Storage.

    """
    db = db_blockstorage.DbBlockStorage(db_dir)

    blkstorage_list = db.list(user_login_delete)

    for blkstorage in blkstorage_list:        
        id = blkstorage[0]
        region = blkstorage[1]
        ocid = blkstorage[2]
        replica_id = blkstorage[3]
        replica_ad = blkstorage[4]
        owner = blkstorage[5]

        oci_config['region'] = region

        oci_blkstorage = oci_blockstorage.OciBlockStorage(oci_config)
        
        if replica_id:
            print('--> Deleting BLOCK STORAGE REPLICA - OCID: %s | Owner: %s | Region: %s' % \
                (replica_id, owner, region,))
            
            replica_deleted = oci_blkstorage.delete_replica(replica_id)

        print('--> Deleting BLOCK STORAGE - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))

        exists = oci_blkstorage.exists(ocid)
    
        if exists:
            deleted = oci_blkstorage.delete_volume(ocid)

            if deleted:
                db.delete(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete(id)

    db.close()


def mysql(oci_config, db_dir, user_login_delete=None):
    """Delete MySQL.

    """
    db = db_mysql.DbMysql(db_dir)

    mysql_list = db.list(user_login_delete)

    for mysql in mysql_list:        
        id = mysql[0]
        region = mysql[1]
        ocid = mysql[2]        
        owner = mysql[3]

        print('--> Deleting MYSQL - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region
        
        oci_db = oci_database.OciDatabase(oci_config)                    
        exists = oci_db.exists_mysql(ocid)
        
        if exists:
            deleted = oci_db.delete_mysql(ocid)

            if deleted:
                db.delete(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete(id)

    db.close()


def fss(oci_config, db_dir, user_login_delete=None):
    """Delete File System Storage (FSS).

    """
    db = db_fss.DbFss(db_dir)
    
    fss_ex_list = db.list_export(user_login_delete)
        
    for export in fss_ex_list:
        id = export[0]
        region = export[1]
        ocid = export[2]
        owner = export[3]
        
        print('--> Deleting FSS (Export) - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_fss = oci_filestorage.OciFileStorage(oci_config)   
        exists = oci_fss.exists_export(ocid)

        if exists:
            deleted = oci_fss.delete_export(ocid)

            if deleted:
                db.delete_export(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete_export(id)
    

    fss_mt_list = db.list_mounttarget(user_login_delete)

    for mounttarget in fss_mt_list:
        id = mounttarget[0]
        region = mounttarget[1]
        ocid = mounttarget[2]
        owner = mounttarget[3]
        
        print('--> Deleting FSS (Mount Target) - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_fss = oci_filestorage.OciFileStorage(oci_config)   
        exists = oci_fss.exists_mounttarget(ocid)

        if exists:
            deleted = oci_fss.delete_mounttarget(ocid)

            if deleted:
                db.delete_mounttarget(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete_mounttarget(id)


    fss_fs_list = db.list_filesystem(user_login_delete)

    for filesystem in fss_fs_list:
        id = filesystem[0]
        region = filesystem[1]
        ocid = filesystem[2]
        owner = filesystem[3]
        
        print('--> Deleting FSS (File System) - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_fss = oci_filestorage.OciFileStorage(oci_config)   
        exists = oci_fss.exists_filesystem(ocid)

        if exists:
            deleted = oci_fss.delete_filesystem(ocid)

            if deleted:
                db.delete_filesystem(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete_filesystem(id)

            
    db.close()

    
    
