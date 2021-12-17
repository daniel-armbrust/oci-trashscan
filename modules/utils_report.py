#
# modules/utils_report.py
#

from . import db_adb
from . import db_odb
from . import db_compute
from . import db_blockstorage
from . import db_mysql
from . import db_fss
    

def adb(db_dir, html_file_obj):
    """Generate HTML report from Autonomous Databases.

    """
    print('--> Report: AUTONOMOUS DATABASE (adb).')

    db = db_adb.DbAdb(db_dir)
    adbs_list = db.list()
    db.close()

    html_table = '''
       <h2><u>Autonomous Databases</u></h2>
       <table border="1">
          <thead>
              <tr>
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>oCPU</th><th>Storage (gbs)</th><th>Storage (tbs)</th>
                 <th>Workload Type</th><th>OCID</th><th>Owner</th><th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for adb in adbs_list:
       html_table = '<tr>'
       
       for i in range(len(adb)):
           html_table += '<td>%s</td>' % (adb[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)


def odb(db_dir, html_file_obj):
    """Generate HTML report from Oracle Datbases.

    """
    print('--> Report: ORACLE DATABASE (odb).')

    db = db_odb.DbOdb(db_dir)
    odbs_list = db.list()
    db.close()

    html_table = '''
       <h2><u>Oracle Databases</u></h2>
       <table border="1">
          <thead>
              <tr>
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>Edition</th><th>Shape</th><th>Storage (gbs)</th><th>OCID</th>
                 <th>Owner</th><th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for odb in odbs_list:
       html_table = '<tr>'
       
       for i in range(len(odb)):
           html_table += '<td>%s</td>' % (odb[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)


def compute(db_dir, html_file_obj):
    """Generate HTML report from Compute Instances.

    """
    print('--> Report: COMPUTE INSTANCE.')

    db = db_compute.DbCompute(db_dir)
    computes_list = db.list_computes()
    db.close()

    html_table = '''
       <h2><u>Compute Instances</u></h2>
       <table border="1">
          <thead>
              <tr>
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>AD</th><th>Shape</th><th>OCID</th><th>Owner</th>
                 <th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for compute in computes_list:
       html_table = '<tr>'
       
       for i in range(len(compute)):
           html_table += '<td>%s</td>' % (compute[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)


def custom_image(db_dir, html_file_obj):
    """Generate HTML report from Custom Images.

    """
    print('--> Report: CUSTOM IMAGE.')

    db = db_compute.DbCompute(db_dir)
    imgs_list = db.list_custom_images()
    db.close()

    html_table = '''   
       <h2><u>Custom Image</u></h2>
       <table border="1">
          <thead>
              <tr>
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>OCID</th><th>Billable (gbs)</th><th>Operating System</th><th>Version</th>
                 <th>Size (mbs)</th><th>Owner</th><th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for image in imgs_list:
       html_table = '<tr>'
       
       for i in range(len(image)):
           html_table += '<td>%s</td>' % (image[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)


def blockstorage(db_dir, html_file_obj):
    """Generate HTML report from Block Storage.

    """
    print('--> Report: BLOCK STORAGE.')

    db = db_blockstorage.DbBlockStorage(db_dir)
    blkstorages_list = db.list()
    db.close()

    html_table = '''   
       <h2><u>Block Storage</u></h2>
       <table border="1">
          <thead>
              <tr>              
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>AD</th><th>Size (gbs)</th><th>Size (mbs)</th><th>VPUS per GB</th>
                 <th>Replica ID</th><th>Replica AD</th><th>OCID</th><th>Owner</th>
                 <th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for blkstorage in blkstorages_list:
       html_table = '<tr>'
       
       for i in range(len(blkstorage)):
           html_table += '<td>%s</td>' % (blkstorage[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)


def mysql(db_dir, html_file_obj):
    """Generate HTML report from MySQL.

    """
    print('--> Report: MYSQL.')

    db = db_mysql.DbMysql(db_dir)
    mysql_list = db.list()
    db.close()

    html_table = '''   
       <h2><u>MySQL</u></h2>
       <table border="1">
          <thead>
              <tr>                        
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>Version</th><th>Shape</th><th>HA</th><th>OCID</th><th>Owner</th>
                 <th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for mysql in mysql_list:
       html_table = '<tr>'
       
       for i in range(len(mysql)):
           html_table += '<td>%s</td>' % (mysql[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)


def fss(db_dir, html_file_obj):
    """Generate HTML report from File System Storage (FSS).

    """
    print('--> Report: FSS (File System).')

    db = db_fss.DbFss(db_dir)
    fss_fs_list = db.list_filesystems()
    
    html_table = '''   
       <h2><u>File System Storage (FSS)</u></h2>
       <h3><u>FileSystem</u></h3>
       <table border="1">
          <thead>
              <tr>
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>AD</th><th>OCID</th><th>Owner</th><th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for fss_fs in fss_fs_list:
       html_table = '<tr>'
       
       for i in range(len(fss_fs)):
           html_table += '<td>%s</td>' % (fss_fs[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)

    print('--> Report: FSS (Mount Target).')

    fss_mt_list = db.list_mounttargets()

    html_table = '''          
       <h3><u>Mount Target</u></h3>
       <table border="1">
          <thead>
              <tr>
                 <th>ID</th><th>Region</th><th>Compartment</th><th>Name</th>
                 <th>AD</th><th>OCID</th><th>Subnet ID</th><th>Owner</th>
                 <th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for fss_mt in fss_mt_list:
       html_table = '<tr>'
       
       for i in range(len(fss_mt)):
           html_table += '<td>%s</td>' % (fss_mt[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)

    print('--> Report: FSS (Snapshot).')

    fss_snp_list = db.list_snapshots()

    html_table = '''          
       <h3><u>Snapshot</u></h3>
       <table border="1">
          <thead>
              <tr>
                 <th>ID</th><th>Region</th><th>OCID</th><th>Name</th>
                 <th>FileSystem ID</th><th>Provenance ID</th><th>Owner</th>
                 <th>Created On</th>
              </tr>
          </thead>
          <tbody>
    '''

    html_file_obj.write(html_table)

    for fss_snp in fss_snp_list:
       html_table = '<tr>'
       
       for i in range(len(fss_snp)):
           html_table += '<td>%s</td>' % (fss_snp[i],)

       html_table += '</tr>'

       html_file_obj.write(html_table)        

    html_table = '</tbody></table>'
    html_file_obj.write(html_table)

    db.close()