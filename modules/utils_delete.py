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

    adbs_list = db.list(user_login_delete)

    for adb in adbs_list:
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
    db = db_odb.DbOdb(db_dir)

    odbs_list = db.list(user_login_delete)

    for odb in odbs_list:
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

    computes_list = db.list_computes(user_login_delete)

    for compute in computes_list:
        id = compute[0]
        region = compute[1]
        ocid = compute[2]
        owner = compute[3]

        print('--> Deleting COMPUTE INSTANCE - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_cpt = oci_compute.OciCompute(oci_config)
        exists = oci_cpt.exists_compute(ocid)

        if exists:
            deleted = oci_cpt.terminate(ocid)

            if deleted:
                db.delete_compute(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete_compute(id)
    
    db.close()


def custom_image(oci_config, db_dir, user_login_delete=None):
    """Delete Custom Images.

    """
    db = db_compute.DbCompute(db_dir)

    custom_imgs_list = db.list_custom_images(user_login_delete)

    for custom_img in custom_imgs_list:
        id = custom_img[0]
        region = custom_img[1]
        ocid = custom_img[2]
        owner = custom_img[3]

        print('--> Deleting CUSTOM IMAGE - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_cimage = oci_compute.OciCompute(oci_config)
        exists = oci_cimage.exists_custom_image(ocid)

        if exists:
            deleted = oci_cimage.delete_custom_image(ocid)

            if deleted:
                db.delete_custom_image(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete_custom_image(id)
    
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
    
    fss_snp_list = db.list_snapshots(user_login_delete)
        
    for snapshot in fss_snp_list:
        id = snapshot[0]
        region = snapshot[1]
        ocid = snapshot[2]
        owner = snapshot[3]
        
        print('--> Deleting FSS (Snapshot) - OCID: %s | Owner: %s | Region: %s' % \
            (ocid, owner, region,))
        
        oci_config['region'] = region

        oci_fss = oci_filestorage.OciFileStorage(oci_config)   
        exists = oci_fss.exists_snapshot(ocid)

        if exists:
            deleted = oci_fss.delete_snapshot(ocid)

            if deleted:
                db.delete_snapshot(id)
            else:
                print('\t!!! The resource was not deleted on OCI!\n')                
        else:
            db.delete_snapshot(id)    

    fss_mt_list = db.list_mounttargets(user_login_delete)

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


    fss_fs_list = db.list_filesystems(user_login_delete)

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

    
    
