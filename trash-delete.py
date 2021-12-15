#
# trash-delete.py
#

import sys
import os
import getopt
from multiprocessing import Process

import oci

from modules import oci_identity
from modules import utils_delete

#
# Globals
#  
TRASH_DELETE_VERSION = '1.0b'
LICENSE = 'GPLv3'
AUTHOR = 'Daniel Armbrust <darmbrust@gmail.com>'


def logo():
    logo_text = '''
    LADCLOUDADOPTION Trash-Delete 
    =============================

    Version.........: %s
    License.........: %s
    Author..........: %s
    
    ''' % (TRASH_DELETE_VERSION, LICENSE, AUTHOR)

    print(logo_text)


def show_help():
    logo()

    help_text = '''   
    Options:
       -h, --help           Show this help and exit.

       -c                   The path of the OCI config file (default to: ~/.oci/config)          
       -u                   Specify the username to delete resources (default to: all users)
              
    '''

    print(help_text + '\n')


def init_oci_sdk(config_file='~/.oci/config', region=None):    
    config = oci.config.from_file(file_location=config_file)    
    oci.config.validate_config(config)
    
    return config


def start_trash_delete(oci_config_file, db_dir, user_login_delete):
    """Function that starts the delete of resources.

    """
    #service_func_list = [utils_delete.adb, utils_delete.odb, utils_delete.compute,
    #     utils_delete.custom_image, utils_delete.blockstorage, utils_delete.mysql, 
    #     utils_delete.fss, utils_delete.oke, utils_delete.analytics, utils_scan.goldengate]
    service_func_list = [utils_delete.adb]

    logo()
    print('*** Starting DELETING resources...\n')

    oci_config = init_oci_sdk(oci_config_file)

    for service_func in service_func_list:
        service_func(oci_config, db_dir, user_login_delete)


def main(argv):
    """Main execution. Parse the command line.
    
    """
    oci_config_file = '~/.oci/config'
    
    db_dir = os.getcwd() + '/db'       

    user_login_delete = None

    try:
        opts, args = getopt.getopt(argv, 'hc:u:', [])
    except getopt.GetoptError:
        show_help()
        sys.exit(1)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            show_help()
            sys.exit(0)
        elif opt in ('-c',):
            oci_config_file = arg
        elif opt in ('-u',):
            user_login_delete = arg
            

    if not os.path.isdir(db_dir):
        print('[ERROR] The database directory "%s" does not exists!' % (db_dir,))
        sys.exit(1)

    if not os.path.exists(oci_config_file):        
        show_help()
        print('[ERROR] Cannot find the OCI config file: "%s"' % (oci_config_file,))
        sys.exit(1)  

    start_trash_delete(oci_config_file, db_dir, user_login_delete)

    print('\n\nFinish...')
    sys.exit(0)    


if __name__ == '__main__':
    main(sys.argv[1:])
else:
    sys.exit(1)