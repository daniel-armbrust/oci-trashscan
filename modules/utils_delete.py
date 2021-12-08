#
# modules/utils_delete.py
#

from . import oci_compute

from . import db_compute


def compute(oci_config, db_dir, user_login_delete):
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
                pass
        else:
            db.delete(id)

    
    db.close()