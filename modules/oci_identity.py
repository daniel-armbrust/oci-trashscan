#
# modules/oci_identity.py
#

from oci import identity


class Identity():
    """ Class for manipulating the OCI IAM Service.

    """
    def __init__(self, oci_config):
        self._idc = identity.IdentityClient(oci_config)
        

    def list_all_compartments(self, tenant_id):
        """ Return a list of all ACTIVE compartments from the Tenant.
                
        """                
        cmp_list = []
        next_page_id = ''

        while True:
            resp = self._idc.list_compartments(compartment_id=tenant_id, lifecycle_state='ACTIVE', 
                compartment_id_in_subtree=True, page=next_page_id)

            for resp_data in resp.data:
                cmp_list.append(resp_data)
            
            if resp.has_next_page:
                next_page_id = resp.next_page
            else:
                break  

        return cmp_list
    
    
    def list_my_regions(self, tenant_id):
        """ Lists all region subscriptions for the specified tenancy.

        """
        region_list = []

        resp = self._idc.list_region_subscriptions(tenant_id)

        for resp_data in resp.data:
            region_list.append(resp_data.region_name)
        
        return region_list
    

    def get_home_region(self, tenant_id):
        """ Return the name of my home region.
        
        """
        home_region = ''

        resp = self._idc.list_region_subscriptions(tenant_id)

        for resp_data in resp.data:
            if resp_data.is_home_region:
                home_region = resp_data.region_name
                    
        return home_region


        
