#
# modules/utils.py
#

from . import oci_identity
from . import oci_database
from . import oci_compute
from . import oci_blockstorage
from . import oci_filestorage
from . import oci_oke
from . import oci_analytics
from . import oci_goldengate

from . import db_adb
from . import db_odb
from . import db_mysql
from . import db_compute
from . import db_blockstorage
from . import db_fss
from . import db_analytics

    
def adb(oci_config, db_dir, compartment_props):
    """Scan Autonomous Databases.

    """
    adb_dict = {'region': '', 'compartment_id': '', 'name': '', 'ocpu': 0, 
        'storage_gbs': 0, 'storage_tbs': 0, 'workload_type': '', 
        'ocid': '', 'owner': '', 'created_on': ''}
    
    adb_list = []

    print('--> Scanning AUTONOMOUS DATABASE (adb) - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))

    oci_db = oci_database.OciDatabase(oci_config)    
    adb_list = oci_db.list_adbs(compartment_props.id)
    
    db = db_adb.DbAdb(db_dir)

    for adb_props in adb_list:
        adb_dict['region'] = oci_config['region']
        adb_dict['compartment_id'] = adb_props.compartment_id
        adb_dict['name'] = adb_props.display_name
        adb_dict['ocpu'] = adb_props.cpu_core_count
        adb_dict['storage_gbs'] = adb_props.data_storage_size_in_gbs
        adb_dict['storage_tbs'] = adb_props.data_storage_size_in_tbs
        adb_dict['workload_type'] = adb_props.db_workload        
        adb_dict['ocid'] = adb_props.id

        try:
            adb_dict['owner'] = adb_props.defined_tags['Oracle-Tags']['CreatedBy']
            adb_dict['created_on'] = adb_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass
        
        db.add(adb_dict)

    db.close()


def odb(oci_config, db_dir, compartment_props):
    """Scan Oracle Datbases.

    """
    odb_dict = {'region': '', 'compartment_id': '', 'name': '', 'edition': '', 
        'shape': '', 'storage_gbs': 0, 'ocid': '', 'owner': '', 'created_on': ''}

    print('--> Scanning ORACLE DATABASE (odb) - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
      
    oci_db = oci_database.OciDatabase(oci_config)    
    odb_list = oci_db.list_odbs(compartment_props.id)
    
    db = db_odb.DbOdb(db_dir)

    for odb_props in odb_list:
        odb_dict['region'] = oci_config['region']
        odb_dict['compartment_id'] = odb_props.compartment_id
        odb_dict['name'] = odb_props.display_name
        odb_dict['edition'] = odb_props.database_edition
        odb_dict['shape'] = odb_props.shape
        odb_dict['storage_gbs'] = odb_props.data_storage_size_in_gbs        
        odb_dict['ocid'] = odb_props.id

        try:
            odb_dict['owner'] = odb_props.defined_tags['Oracle-Tags']['CreatedBy']
            odb_dict['created_on'] = odb_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass
        
        db.add(odb_dict)

    db.close()


def compute(oci_config, db_dir, compartment_props):
    """Scan Compute Instances and Custom Images.

    """
    compute_dict = {'region': '', 'compartment_id': '', 'name': '', 'ad': '',
        'shape': '', 'ocid': '', 'owner': '', 'created_on': ''}   
   
    print('--> Scanning COMPUTE INSTANCES - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
    
    oci_cpt = oci_compute.OciCompute(oci_config)
    cpt_list = oci_cpt.list_computes(compartment_props.id)    

    db = db_compute.DbCompute(db_dir)

    for cpt_props in cpt_list:
        compute_dict['region'] = oci_config['region']
        compute_dict['compartment_id'] = cpt_props.compartment_id
        compute_dict['name'] = cpt_props.display_name
        compute_dict['ad'] = cpt_props.availability_domain
        compute_dict['lifecycle_state'] = cpt_props.lifecycle_state
        compute_dict['shape'] = cpt_props.shape
        compute_dict['ocid'] = cpt_props.id

        try:
            compute_dict['owner'] = cpt_props.defined_tags['Oracle-Tags']['CreatedBy']
            compute_dict['created_on'] = cpt_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass

        db.add_compute(compute_dict)   

    db.close()


def custom_image(oci_config, db_dir, compartment_props):
    """Scan Custom Images.

    """
    custom_img_dict = {'region': '', 'compartment_id': '', 'billable_size_in_gbs': 0,
        'name': '', 'ocid': '', 'operating_system': '', 'operating_system_version': '',
        'size_in_mbs': 0, 'owner': '', 'created_on': ''}

    print('--> Scanning CUSTOM IMAGES - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
    
    oci_cpt = oci_compute.OciCompute(oci_config)
    custom_imgs_list = oci_cpt.list_custom_images(compartment_props.id)

    db = db_compute.DbCompute(db_dir)

    for imgs_props in custom_imgs_list:
        custom_img_dict['region'] = oci_config['region']
        custom_img_dict['compartment_id'] = imgs_props.compartment_id
        custom_img_dict['name'] = imgs_props.display_name
        custom_img_dict['billable_size_in_gbs'] = imgs_props.billable_size_in_gbs
        custom_img_dict['ocid'] = imgs_props.id
        custom_img_dict['operating_system'] = imgs_props.operating_system
        custom_img_dict['operating_system_version'] = imgs_props.operating_system_version        
        custom_img_dict['size_in_mbs'] = imgs_props.size_in_mbs        

        try:
            custom_img_dict['owner'] = imgs_props.defined_tags['Oracle-Tags']['CreatedBy']
            custom_img_dict['created_on'] = imgs_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass

        db.add_custom_image(custom_img_dict)

    db.close()


def blockstorage(oci_config, db_dir, compartment_props):
    """Scan Block Storage.

    """
    blockstorage_dict = {'region': '', 'compartment_id': '', 'name': '', 'ad': '', 
        'size_gbs': 0, 'size_mbs': 0, 'vpus_per_gb': 0, 'ocid': '', 'replica_id': '', 
        'replica_ad': '', 'owner': '', 'created_on': ''}

    print('--> Scanning BLOCK STORAGE - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
    
    oci_blkstorage = oci_blockstorage.OciBlockStorage(oci_config)
    blkstorage_list = oci_blkstorage.list_volumes(compartment_props.id)

    db = db_blockstorage.DbBlockStorage(db_dir)

    for blkstr_props in blkstorage_list:
        blockstorage_dict['region'] = oci_config['region']
        blockstorage_dict['compartment_id'] = blkstr_props.compartment_id
        blockstorage_dict['name'] = blkstr_props.display_name
        blockstorage_dict['ad'] = blkstr_props.availability_domain        
        blockstorage_dict['size_gbs'] = blkstr_props.size_in_gbs
        blockstorage_dict['size_mbs'] = blkstr_props.size_in_mbs
        blockstorage_dict['vpus_per_gb'] = blkstr_props.vpus_per_gb
        blockstorage_dict['ocid'] = blkstr_props.id

        if hasattr(blkstr_props, 'block_volume_replicas') and not (type(blkstr_props.block_volume_replicas) == None.__class__):            
            blockstorage_dict['replica_id'] = blkstr_props.block_volume_replicas[0].block_volume_replica_id
            blockstorage_dict['replica_ad'] = blkstr_props.block_volume_replicas[0].availability_domain

        try:
            blockstorage_dict['owner'] = blkstr_props.defined_tags['Oracle-Tags']['CreatedBy']
            blockstorage_dict['created_on'] = blkstr_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass

        db.add(blockstorage_dict)
    
    db.close()


def mysql(oci_config, db_dir, compartment_props):
    """Scan MySQL.

    """
    mysql_dict = {'region': '', 'compartment_id': '', 'name': '', 'version': '', 
        'shape': '', 'highly_available': '', 'ocid': '', 'owner': '', 
        'created_on': ''}

    print('--> Scanning MYSQL - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
    
    oci_db = oci_database.OciDatabase(oci_config)    
    mysql_list = oci_db.list_mysqls(compartment_props.id)
    
    db = db_mysql.DbMysql(db_dir)

    for mysql_props in mysql_list:
        mysql_details = oci_db.get_mysql(mysql_props.id)

        mysql_dict['region'] = oci_config['region']
        mysql_dict['compartment_id'] = mysql_props.compartment_id
        mysql_dict['name'] = mysql_props.display_name
        mysql_dict['version'] = mysql_props.mysql_version
        mysql_dict['shape'] = mysql_details.shape_name
        mysql_dict['highly_available'] = mysql_props.is_highly_available        
        mysql_dict['ocid'] = mysql_props.id

        try:
            mysql_dict['owner'] = mysql_props.defined_tags['Oracle-Tags']['CreatedBy']
            mysql_dict['created_on'] = mysql_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass

        db.add(mysql_dict)

    db.close()
      

def fss(oci_config, db_dir, compartment_props):
    """Scan File System Storage (FSS).

    """
    fss_fs_dict = {'region': '', 'compartment_id': '', 'name': '', 'ad': '',
        'ocid': '', 'owner': '', 'created_on': ''}
    
    fss_snp_dict = {'region': '', 'file_system_id': '', 'name': '', 'provenance_id': '',
        'ocid': '', 'owner': '', 'created_on': ''}
    
    fss_exp_dict = {'region': '', 'compartment_id': '', 'export_set_id': '', 
        'file_system_id': '', 'ocid': ''}
    
    fss_mt_dict = {'region': '', 'compartment_id': '', 'name': '', 'ad': '',
        'subnet_id': '', 'ocid': ''}

    print('--> Scanning FSS - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
 
    idt = oci_identity.Identity(oci_config)
    ad_list = idt.list_ads(compartment_props.id)

    oci_fss = oci_filestorage.OciFileStorage(oci_config)   

    fssfs_ad_list = []    
    fssmt_ad_list = []
    fssexp_list = []
    fsssnp_list = []

    for ad in ad_list:
        # FileStorage FileSystem
        fss_fs_list = oci_fss.list_filesystems(compartment_id=compartment_props.id, ad=ad)        

        for resp in fss_fs_list:             
            fssfs_ad_list.append(resp)
            fssfs_id = resp.id

            # FileStorage SNAPSHOT
            fss_snp_list = oci_fss.list_snapshots(fssfs_id)            

            for resp in fss_snp_list:
                fsssnp_list.append(resp)

        # FileStorage MOUNTTARGET
        fss_mt_list = oci_fss.list_mounttargets(compartment_id=compartment_props.id, ad=ad)

        for resp in fss_mt_list:
            fssmt_ad_list.append(resp)

    # FileStorage EXPORTS 
    fss_ex_list = oci_fss.list_exports(compartment_id=compartment_props.id)

    for resp in fss_ex_list:            
        fssexp_list.append(resp)
    
    db = db_fss.DbFss(db_dir)

    for fss_props in fssfs_ad_list:
        fss_fs_dict['region'] = oci_config['region']
        fss_fs_dict['compartment_id'] = fss_props.compartment_id
        fss_fs_dict['name'] = fss_props.display_name
        fss_fs_dict['ad'] = fss_props.availability_domain
        fss_fs_dict['ocid'] = fss_props.id     

        try:
            fss_fs_dict['owner'] = fss_props.defined_tags['Oracle-Tags']['CreatedBy']
            fss_fs_dict['created_on'] = fss_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass

        db.add_filesystem(fss_fs_dict)
    
    for fss_props in fsssnp_list:
        fss_snp_dict['region'] = oci_config['region']
        fss_snp_dict['file_system_id'] = fss_props.file_system_id
        fss_snp_dict['name'] = fss_props.name
        fss_snp_dict['provenance_id'] = fss_props.provenance_id
        fss_snp_dict['ocid'] = fss_props.id        

        try:
            fss_snp_dict['owner'] = fss_props.defined_tags['Oracle-Tags']['CreatedBy']
            fss_snp_dict['created_on'] = fss_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            pass

        db.add_snapshot(fss_snp_dict)

    for fss_props in fssexp_list:
        fss_exp_dict['region'] = oci_config['region']
        fss_exp_dict['compartment_id'] = fss_props.compartment_id
        fss_exp_dict['export_set_id'] = fss_props.export_set_id
        fss_exp_dict['file_system_id'] = fss_props.file_system_id
        fss_exp_dict['ocid'] = fss_props.id        

        db.add_export(fss_exp_dict)
    
    for fss_props in fssmt_ad_list:
        fss_mt_dict['region'] = oci_config['region']
        fss_mt_dict['compartment_id'] = fss_props.compartment_id
        fss_mt_dict['name'] = fss_props.display_name
        fss_mt_dict['ad'] = fss_props.availability_domain
        fss_mt_dict['subnet_id'] = fss_props.subnet_id
        fss_mt_dict['ocid'] = fss_props.id        

        db.add_mounttarget(fss_mt_dict)
    
    db.close()


def oke(oci_config, db_dir, compartment_props):
    """Scan Container Engine for Kubernetes (OKE).

    """

    print('--> Scanning OKE - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))

    oke = oci_oke.OciOke(oci_config)
    oke_cluster_list = oke.list_clusters(compartment_id=compartment_props.id)

    print(oke_cluster_list)


def analytics(oci_config, db_dir, compartment_props):
    """Scan Analytics instances.

    """
    analytics_dict = {'region': '', 'compartment_id': '', 'name': '', 'capacity_type': '',
        'capacity_value': '', 'feature_set': '', 'ocid': '', 'license_type': '', 
        'owner': '', 'created_on': ''}

    print('--> Scanning ANALYTICS - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))

    analytics = oci_analytics.OciAnalytics(oci_config)
    analytics_list = analytics.list_instances(compartment_id=compartment_props.id)

    db = db_analytics.DbAnalytics(db_dir)

    for analytics_props in analytics_list:
        analytics_dict['region'] = oci_config['region']
        analytics_dict['compartment_id'] = analytics_props.compartment_id
        analytics_dict['name'] = analytics_props.name
        analytics_dict['capacity_type'] = analytics_props.capacity.capacity_type
        analytics_dict['capacity_value'] = analytics_props.capacity.capacity_value
        analytics_dict['feature_set'] = analytics_props.feature_set        
        analytics_dict['ocid'] = analytics_props.id
        analytics_dict['license_type'] = analytics_props.license_type

        try:
            analytics_dict['owner'] = analytics_props.defined_tags['Oracle-Tags']['CreatedBy']
            analytics_dict['created_on'] = analytics_props.defined_tags['Oracle-Tags']['CreatedOn']
        except (AttributeError, KeyError,):
            analytics_dict['created_on'] = analytics_props.time_created

        db.add(analytics_dict)
    
    db.close()
    

def goldengate(oci_config, db_dir, compartment_props):
    """Scan GoldenGate.

    """
    gg_dict = {'region': '', 'compartment_id': '', 'name': '', 'capacity_type': '',
        'capacity_value': '', 'feature_set': '', 'ocid': '', 'license_type': '', 
        'owner': '', 'created_on': ''}

    print('--> Scanning GOLDENGATE - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))

    gg = oci_goldengate.OciGoldenGate(oci_config)
    #gg_list = gg.list_deployments(compartment_id=compartment_props.id)
    gg_list = gg.list_database_registrations(compartment_id='ocid1.compartment.oc1..aaaaaaaaeuoahv6qbohyqqxfoj4ku7zlc5oql4a6z7o6xlkrzrjpkrvpmoja')

    print(gg_list)    