#
# modules/oci_identity.py
#

from oci import identity
from oci import retry as oci_retry


class Identity():
    """Class for manipulating the OCI IAM Service.

    """
    def __init__(self, oci_config, timeout=120):
        self.__idc = identity.IdentityClient(oci_config, timeout=timeout)
       
    def list_all_compartments(self, tenant_id):
        """Return a list of all ACTIVE compartments from the Tenant.
                
        """                
        cmp_list = []
        next_page_id = None

        while True:
            resp = self.__idc.list_compartments(compartment_id=tenant_id, lifecycle_state='ACTIVE', 
                compartment_id_in_subtree=True, page=next_page_id,
                retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)

            for resp_data in resp.data:
                cmp_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break  

        return cmp_list
        
    def list_my_regions(self, tenant_id):
        """Lists all region subscriptions for the specified tenancy.

        """
        region_list = []

        resp = self.__idc.list_region_subscriptions(tenancy_id=tenant_id, 
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)

        for resp_data in resp.data:
            region_list.append(resp_data.region_name)
        
        return region_list
    
    def get_home_region(self, tenant_id):
        """Return the name of my home region.
        
        """
        home_region = ''

        resp = self.__idc.list_region_subscriptions(tenancy_id=tenant_id,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)

        for resp_data in resp.data:
            if resp_data.is_home_region:
                home_region = resp_data.region_name
                    
        return home_region

    def list_ads(self, compartment_id):
        """Lists the availability domains in your tenancy.

        """
        ad_list = []

        resp = self.__idc.list_availability_domains(compartment_id=compartment_id,
            retry_strategy=oci_retry.DEFAULT_RETRY_STRATEGY)

        for resp_data in resp.data:
            ad_list.append(resp_data.name)
        
        return ad_list
        
