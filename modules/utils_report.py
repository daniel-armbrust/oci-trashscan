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
    