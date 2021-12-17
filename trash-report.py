#!/usr/bin/env python3
#
# trash-report.py
#

import sys
import os
import getopt
from datetime import datetime

from oci import config as oci_config
from modules import utils_report

#
# Globals
#  
TRASH_REPORT_VERSION = '1.0b'
LICENSE = 'GPLv3'
AUTHOR = 'Daniel Armbrust <darmbrust@gmail.com>'


def logo():
    logo_text = '''
    LADCLOUDADOPTION Trash-Report 
    =============================

    Version.........: %s
    License.........: %s
    Author..........: %s
    
    ''' % (TRASH_REPORT_VERSION, LICENSE, AUTHOR)

    print(logo_text)


def show_help():
    logo()

    help_text = '''   
    Options:
       -h, --help           Show this help and exit.
       
       -d                   Specify the directory where HTML filename report is saved (default to: ./report)
              
    '''

    print(help_text + '\n')


def start_trash_report(db_dir, html_report_path):
    """Function that starts the report of the scanned resources.

    """
    logo()
    print('*** Starting generate REPORT from scanned resources...\n')

    current_date = datetime.now().strftime('%d/%m/%Y')

    report_title = 'LADCLOUDADOPTION Trash-Report %s - %s' % (TRASH_REPORT_VERSION, current_date,)

    html_data = '''<html>
       <head>
          <title>%s</title>
       </head>
       <body>
          <h1>%s</h1>       
    ''' % (report_title, report_title,)
    
    service_func_list = [utils_report.adb, utils_report.odb, utils_report.compute, 
        utils_report.custom_image, utils_report.blockstorage, utils_report.mysql,
        utils_report.fss]

    report_f = open(html_report_path, 'a') 
    report_f.write(html_data)

    for service_func in service_func_list:        
        service_func(db_dir, report_f)    

    html_data = '</body></html>'    
    report_f.write(html_data)

    report_f.close()


def main(argv):
    """Main execution. Parse the command line.
    
    """
    db_dir = os.getcwd() + '/db'

    html_report_dir = './report'
    html_report_file = 'trash-report_' + datetime.now().strftime('%b%d-%Y') + '.html'

    try:
        opts, args = getopt.getopt(argv, 'hc:u:', [])
    except getopt.GetoptError:
        show_help()
        sys.exit(1)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            show_help()
            sys.exit(0)
        elif opt in ('-d',):
            html_report_dir = arg
                    

    if not os.path.isdir(db_dir):
        print('[ERROR] The database directory "%s" does not exists!' % (db_dir,))
        sys.exit(1)

    if not os.path.isdir(html_report_dir):        
        show_help()
        print('[ERROR] The report directory "%s" does not exists!' % (html_report_dir,))
        sys.exit(1)
    else:
        html_report_path = html_report_dir + '/' + html_report_file
        
        if os.path.isfile(html_report_path):
            print('[ERROR] The report file "%s" exists! Please, delete it before continue.' % (html_report_path,))
            sys.exit(1)
        else:
            start_trash_report(db_dir, html_report_path)


    print('\n\nFinish...')
    sys.exit(0)    


if __name__ == '__main__':
    main(sys.argv[1:])
else:
    sys.exit(1)