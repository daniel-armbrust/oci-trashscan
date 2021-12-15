#
# trash-scan.py
#

import sys
import os
import getopt
from multiprocessing import Process

import oci

from modules import oci_identity
from modules import utils_scan

#
# Globals
#  
TRASH_SCAN_VERSION = '1.0b'
LICENSE = 'GPLv3'
AUTHOR = 'Daniel Armbrust <darmbrust@gmail.com>'

def logo():
    logo_text = '''
    LADCLOUDADOPTION Trash-Scan 
    ===========================

    Version.........: %s
    License.........: %s
    Author..........: %s
    
    ''' % (TRASH_SCAN_VERSION, LICENSE, AUTHOR)

    print(logo_text)


def show_help():
    logo()

    help_text = '''   
    Options:
       -h, --help           Show this help and exit.

       -c                   The path of the OCI config file (default to: ~/.oci/config)   
       -r                   Number of OCI Regions to scan in parallel (default to: 2)
              
    '''

    print(help_text + '\n')


def init_oci_sdk(config_file='~/.oci/config', region=None):    
    config = oci.config.from_file(file_location=config_file)    
    oci.config.validate_config(config)
    
    return config


def start_trash_scan(oci_config_file, db_dir, max_regions_parallel):
    """Function that starts the trash scan.

    """    
    #service_func_list = [utils_scan.adb, utils_scan.odb, utils_scan.compute, 
    #    utils_scan.custom_image, utils_scan.blockstorage, utils_scan.mysql, 
    #    utils_scan.fss, utils_scan.oke, utils_scan.analytics, utils_scan.goldengate]
    
    service_func_list = [utils_scan.compute, utils_scan.custom_image]

    logo()
    print('*** Investigating compartments...\n')

    oci_config = init_oci_sdk(oci_config_file)
    tenant_id = oci_config['tenancy']

    idt = oci_identity.Identity(oci_config)

    # List ALL compartments from Tenant
    compartment_list = idt.list_all_compartments(tenant_id)

    # List ALL subscribed regions
    subscrb_regions_list = idt.list_my_regions(tenant_id)  

    for service_func in service_func_list:
        for compartment_props in compartment_list:      
            regions = subscrb_regions_list.copy()

            region_count = 1
            proc_list = []

            while True:
                try:
                    region = regions.pop()
                    oci_config['region'] = region                
                except IndexError:
                    break
                
                p = Process(target=service_func, args=(oci_config, db_dir, compartment_props,))
                p.start()
                proc_list.append(p)
                
                if region_count == max_regions_parallel:
                    for proc in proc_list:
                        proc.join()

                    region_count = 1                    
                    proc_list = []

                    print('\n')
                else:
                    region_count += 1     


def main(argv):
    """Main execution. Parse the command line.
    
    """
    oci_config_file = '~/.oci/config'
    
    db_dir = os.getcwd() + '/db'
    
    max_regions_parallel = 2

    try:
        opts, args = getopt.getopt(argv, 'hc:r:', [])
    except getopt.GetoptError:
        show_help()
        sys.exit(1)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            show_help()
            sys.exit(0)
        elif opt in ('-c',):
            oci_config_file = arg
        elif opt in ('-r',):
            try:            
                max_regions_parallel = int(arg)
            except ValueError:
                show_help()
                sys.exit(1)
            
            if max_regions_parallel < 1:
                show_help()
                sys.exit(1)
      
    if not os.path.isdir(db_dir):
        print('[ERROR] The database directory "%s" does not exists!' % (db_dir,))
        sys.exit(1)

    if not os.path.exists(oci_config_file):        
        show_help()
        print('[ERROR] Cannot find the OCI config file: "%s"' % (oci_config_file,))
        sys.exit(1)  
    
    start_trash_scan(oci_config_file, db_dir, max_regions_parallel)

    print('\n\nFinish...')
    sys.exit(0)    


if __name__ == '__main__':
    main(sys.argv[1:])
else:
    sys.exit(1)