#
# modules/utils.py
#

from . import oci_database
from . import oci_compute
from . import oci_blockstorage

from . import db_adb
from . import db_odb
from . import db_mysql
from . import db_compute

def __line_cleaner():
    for x in range(75):
        print('*' * (75 - x), x, end='\x1b[1K\r')
    
    
def scan_adb(oci_config, db_dir, compartment_props):
    """Scan Autonomous Databases.

    """
    adb_dict = {'region': '', 'compartment_id': '', 'name': '', 'ocpu': 0, 
        'storage_gbs': 0, 'storage_tbs': 0, 'workload_type': '', 'ocid': '',
        'owner': '', 'created_on': ''}
    
    adb_list = []

    print('--> Scanning AUTONOMOUS DATABASE (adb) - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))

    oci_db = oci_database.OciDatabase(oci_config)    
    adb_list = oci_db.list_adb(compartment_props.id)
    
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
        adb_dict['owner'] = adb_props.defined_tags['Oracle-Tags']['CreatedBy']
        adb_dict['created_on'] = adb_props.defined_tags['Oracle-Tags']['CreatedOn']
        
        db.add(adb_dict)

    db.close()


def scan_odb(oci_config, db_dir, compartment_props):
    """Scan Oracle Datbases.

    """
    odb_dict = {'region': '', 'compartment_id': '', 'name': '', 'edition': '', 
        'shape': '', 'storage_gbs': 0, 'ocid': '', 'owner': '', 'created_on': ''}

    print('--> Scanning ORACLE DATABASE (odb) - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
      
    oci_db = oci_database.OciDatabase(oci_config)    
    odb_list = oci_db.list_odb(compartment_props.id)
    
    db = db_odb.DbOdb(db_dir)

    for odb_props in odb_list:
        odb_dict['region'] = oci_config['region']
        odb_dict['compartment_id'] = odb_props.compartment_id
        odb_dict['name'] = odb_props.display_name
        odb_dict['edition'] = odb_props.database_edition
        odb_dict['shape'] = odb_props.shape
        odb_dict['storage_gbs'] = odb_props.data_storage_size_in_gbs        
        odb_dict['ocid'] = odb_props.id
        odb_dict['owner'] = odb_props.defined_tags['Oracle-Tags']['CreatedBy']
        odb_dict['created_on'] = odb_props.defined_tags['Oracle-Tags']['CreatedOn']
        
        db.add(odb_dict)

    db.close()


def scan_compute(oci_config, db_dir, compartment_props):
    """Scan Compute Instances.

    """
    compute_dict = {'region': '', 'compartment_id': '', 'name': '', 'ad': '',
        'lifecycle_state': '', 'shape': '', 'ocid': '', 'owner': '', 'created_on': ''}

    print('--> Scanning COMPUTE INSTANCES - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
    
    oci_cpt = oci_compute.OciCompute(oci_config)
    cpt_list = oci_cpt.list_instances(compartment_props.id)

    db = db_compute.DbCompute(db_dir)

    for cpt_props in cpt_list:
        compute_dict['region'] = oci_config['region']
        compute_dict['compartment_id'] = cpt_props.compartment_id
        compute_dict['name'] = cpt_props.display_name
        compute_dict['ad'] = cpt_props.availability_domain
        compute_dict['lifecycle_state'] = cpt_props.lifecycle_state
        compute_dict['shape'] = cpt_props.shape
        compute_dict['ocid'] = cpt_props.id
        compute_dict['owner'] = cpt_props.defined_tags['Oracle-Tags']['CreatedBy']
        compute_dict['created_on'] = cpt_props.defined_tags['Oracle-Tags']['CreatedOn']

        db.add(compute_dict)

    db.close()


def scan_blockstorage(oci_config, db_dir, compartment_props):
    """Scan Block Storage.

    """
    blockstorage_dict = {'region': '', 'compartment_id': '', 'name': '', 'ad': '', 
        'lifecycle_state': '', 'size_gbs': 0, 'size_mbs': 0, 'vpus_per_gb': 0,
        'ocid': '', 'owner': '', 'created_on': ''}

    print('--> Scanning BLOCK STORAGE - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
    
    oci_blkstorage = oci_blockstorage.OciBlockStorage(oci_config)
    blkstorage_list = oci_blkstorage.list_volumes(compartment_props.id)

    db = db_compute.DbCompute(db_dir)

    for blkstr_props in blkstorage_list:
        blockstorage_dict['region'] = oci_config['region']
        blockstorage_dict['compartment_id'] = blkstr_props.compartment_id
        blockstorage_dict['name'] = blkstr_props.display_name
        blockstorage_dict['ad'] = blkstr_props.availability_domain
        blockstorage_dict['lifecycle_state'] = blkstr_props.lifecycle_state
        blockstorage_dict['size_gbs'] = blkstr_props.size_in_gbs
        blockstorage_dict['size_mbs'] = blkstr_props.size_in_mbs
        blockstorage_dict['vpus_per_gb'] = blkstr_props.vpus_per_gb
        blockstorage_dict['owner'] = blkstr_props.defined_tags['Oracle-Tags']['CreatedBy']
        blockstorage_dict['created_on'] = blkstr_props.defined_tags['Oracle-Tags']['CreatedOn']

        db.add(blockstorage_dict)
    
    db.close()


def scan_mysql(oci_config, db_dir, compartment_props):
    """Scan MySQL.

    """
    mysql_dict = {'region': '', 'compartment_id': '', 'name': '', 'version': '', 
        'shape': '', 'highly_available': '', 'lifecycle_state': '', 'ocid': '', 
        'owner': '', 'created_on': ''}

    print('--> Scanning MYSQL - Comp.: %s (%s) | Region: %s' % \
        (compartment_props.id, compartment_props.name, oci_config['region'],))
    
    oci_db = oci_database.OciDatabase(oci_config)    
    mysql_list = oci_db.list_mysql(compartment_props.id)
    
    db = db_mysql.DbMysql(db_dir)

    for mysql_props in mysql_list:
        mysql_details = oci_db.get_mysql(mysql_props.id)

        mysql_dict['region'] = oci_config['region']
        mysql_dict['compartment_id'] = mysql_props.compartment_id
        mysql_dict['name'] = mysql_props.display_name
        mysql_dict['version'] = mysql_props.mysql_version
        mysql_dict['shape'] = mysql_details.shape_name
        mysql_dict['highly_available'] = mysql_props.is_highly_available
        mysql_dict['lifecycle_state'] = mysql_props.lifecycle_state
        mysql_dict['ocid'] = mysql_props.id
        mysql_dict['owner'] = mysql_props.defined_tags['Oracle-Tags']['CreatedBy']
        mysql_dict['created_on'] = mysql_props.defined_tags['Oracle-Tags']['CreatedOn']

        db.add(mysql_dict)

    db.close()
      

