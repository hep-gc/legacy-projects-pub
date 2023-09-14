'''
Created on May 6, 2014

@author: rd
'''

from __future__ import absolute_import

import itertools
import logging
import thread

from django.conf import settings
import six.moves.urllib.parse as urlparse
from openstack_auth import utils as auth_utils
from pprint import pprint
#import glanceclient as glance_client
from keystoneclient.v2_0 import client

from horizon.utils import functions as utils

from openstack_dashboard.api import base


LOG = logging.getLogger(__name__)

# Set up our data structure for managing Identity API versions, and
# add a couple utility methods to it.
class IdentityAPIVersionManager(base.APIVersionManager):
    def upgrade_v2_user(self, user):
        if getattr(user, "project_id", None) is None:
            user.project_id = getattr(user, "tenantId", None)
        return user

    def get_project_manager(self, *args, **kwargs):
        if VERSIONS.active < 3:
            manager = keystoneclient(*args, **kwargs).tenants
        else:
            manager = keystoneclient(*args, **kwargs).projects
        return manager


VERSIONS = IdentityAPIVersionManager(
    "identity", preferred_version=auth_utils.get_keystone_version())


# Import from oldest to newest so that "preferred" takes correct precedence.
try:
    from keystoneclient.v2_0 import client as keystone_client_v2
    VERSIONS.load_supported_version(2.0, {"client": keystone_client_v2})
except ImportError:
    pass

# Mapping of V2 Catalog Endpoint_type to V3 Catalog Interfaces
ENDPOINT_TYPE_TO_INTERFACE = {
    'publicURL': 'public',
    'internalURL': 'internal',
    'adminURL': 'admin',
}

def get_version_from_service(service):
    if service:
        endpoint = service['endpoints'][0]
        if 'interface' in endpoint:
            return 3
        else:
            return 2.0
    return 2.0

def get_url_for_service(service, region, endpoint_type):
    identity_version = get_version_from_service(service)
    for endpoint in service['endpoints']:
        # ignore region for identity
        if service['type'] == 'identity' or region == endpoint['region']:
            print "Found Url"
            try:
                if identity_version < 3:
                    print "found endpoint%s:%s:%s"%(endpoint_type,endpoint,endpoint[endpoint_type])
                    return endpoint[endpoint_type]
                else:
                    interface = \
                        ENDPOINT_TYPE_TO_INTERFACE.get(endpoint_type, '')
                    if endpoint['interface'] == interface:
                        return endpoint['url']
            except (IndexError, KeyError):
                return None
    return None

def get_service_from_catalog(catalog, service_type):
    if catalog:
        for service in catalog:
            if service['type'] == service_type:
                return service
    return None

def get_glint_url_and_token(request):
    catalog = request.user.service_catalog
    service = get_service_from_catalog(catalog, 'image_mgt')
    region = request.user.services_region
    url = get_url_for_service(service, region, 'publicURL')
    #pprint("found url as %s"%url)
    return eval("{'url':'%s','token':'%s'}"%(url,request.user.token.id) )
    
def keystoneclient(request):
    o = urlparse.urlparse(base.url_for(request, 'identity'))
    r = urlparse.urlparse(base.url_for(request, 'image_mgt'))
    url = "://".join((o.scheme, o.netloc))
    url_r = "://".join((r.scheme, r.netloc))
    bits = urlparse.urlparse(url)
    root = "://".join((bits.scheme, bits.netloc))
    url = "%s/v%s" % (root, VERSIONS.active)
    #url = url.replace("5000", "35357")
    #insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    #cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)
    LOG.debug('glintclient connection created using token "%s" and url "%s"'
              % (request.user.token.id, url))
    pprint('keystoneclient connection created using token "%s" and url "%s"'
              % (request.user.token.id, url))
    pprint("url object %s"%url_r)
    return client.Client( token=request.user.token.id,endpoint=url)




