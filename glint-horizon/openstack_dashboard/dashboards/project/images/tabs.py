'''
Created on Apr 14, 2014

@author: rd
'''
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
# Copyright 2012 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.api import glint

import json
#from openstack_dashboard.api import network

from openstack_dashboard.dashboards.project.images.\
    security_groups.tables import SecurityGroupsTable

from openstack_dashboard.dashboards.project.images.distribution.tables import DistributionTable 

from openstack_dashboard.dashboards.project.images.images \
    import tables as images_tables
    
from openstack_dashboard.dashboards.project.images.image_dist import site_tables 

import requests,ast
#from keystoneclient.v2_0 import client
from pprint import pprint


#class SecurityGroupsTab(tabs.TableTab):
#    table_classes = (SecurityGroupsTable,)
#    name = _("Security Groups")
#    slug = "security_groups_tab"
#    template_name = "horizon/common/_detail_table.html"#

#    def get_security_groups_data(self):
#        try:
#            security_groups = network.security_group_list(self.request)
#        except Exception:
#            security_groups = []
#            exceptions.handle(self.request,
#                              _('Unable to retrieve security groups.'))
#        return security_groups

class ImagesTab(tabs.TableTab):
    table_classes = (images_tables.ImagesTable,)
    name = _("Local Images")
    slug = "images_tab"
    template_name = "horizon/common/_detail_table.html"

    def has_more_data(self, table):
        return getattr(self, "_more_%s" % table.name, False)

    def get_images_data(self):
        marker = self.request.GET.get( images_tables.ImagesTable._meta.pagination_param, None )
        try:
            #images = []
            (images, self._more_images) = api.glance.image_list_detailed(self.request, marker=marker)
        except Exception:
            pprint("exception occurred")
            images = []
            exceptions.handle(self.request, _("Unable to retrieve images."))
        return images

class ImageDistributionTab(tabs.Tab):
    name = _("Image Distribution")
    slug = "imagedistribution_tab"
    #template_name = "horizon/common/_showthis.html"
    template_name = "project/images/image_dist/imagedistribution.html"
    
    def get_context_data(self,request):
        #print("-%s:%s"%(request.user.token.tenant,request.user))
        
        result = glint.get_glint_url_and_token(self.request) 
        
        data_json = requests.post("%simagedistribution/"%result['url'],data={"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
        #print "received %s "%data_json
        data_obj = json.loads(data_json)
        
        return {'data':data_obj}

class Object(object):
    pass

class RemoteRepositoryTab(tabs.TableTab):
    table_classes = (site_tables.SitesTable,)
    name = _("Remote Repositories")
    slug = "remote_repos_tab"
    template_name = "horizon/common/_detail_table.html"

    def has_more_data(self, table):
        return getattr(self, "_more_%s" % table.name, False)

    def get_sites_data(self):
        #marker = self.request.GET.get( site_tables.SitesTable._meta.pagination_param, None )
        try:
            site = []
            result = glint.get_glint_url_and_token(self.request) 
            data_json = requests.post("%slistsites/"%result['url'],data={"USER_ID":self.request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":self.request.user.token.tenant['name']},cookies=None).text
            data_obj = json.loads(data_json)
            
            for idx,s in enumerate(data_obj):
                sobj = json.loads(s)
                
                obj=Object()
                obj.id=sobj['pk']
                obj.url=sobj['url']
                obj.type=sobj['type']
                obj.authport=sobj['authport']
                obj.site_name=sobj['name']
                site.append(obj)
                
            
            #site_tables.site_data=site
            
        except Exception:
            pprint("exception occurred")
            #images = []
            exceptions.handle(self.request, _("Unable to retrieve images."))
        
        return site

class ImageTabs(tabs.TabGroup):
    slug = "access_security_tabs"
    tabs = ( ImagesTab, RemoteRepositoryTab,ImageDistributionTab)
    sticky = True