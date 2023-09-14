'''
Created on May 20, 2014

@author: rd
'''
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
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

from collections import defaultdict

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import defaultfilters as filters
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard import api
from openstack_dashboard.api import base

from openstack_dashboard.api import glint

import requests,json,logging

NOT_LAUNCHABLE_FORMATS = ['aki', 'ari']

site_data=[]
site_index=0

#logging.basicConfig(filename='hor.log',level=eval('Info'),format='%(asctime)s %(message)s')
 
    
class LaunchImage(tables.LinkAction):
    name = "launch_image"
    verbose_name = _("Launch")
    url = "horizon:project:instances:launch"
    classes = ("btn-launch", "ajax-modal")
    policy_rules = (("compute", "compute:create"),)

    def get_link_url(self, datum):
        base_url = reverse(self.url)

        if get_image_type(datum) == "image":
            source_type = "image_id"
        else:
            source_type = "instance_snapshot_id"

        params = urlencode({"source_type": source_type,
                            "source_id": self.table.get_object_id(datum)})
        return "?".join([base_url, params])

    def allowed(self, request, image=None):
        if image and image.container_format not in NOT_LAUNCHABLE_FORMATS:
            return image.status in ("active",)
        return False

class AddCredential(tables.LinkAction):
    #name = "credential"
    #verbose_name = _("Add Credential")
    #url = "horizon:project:images:images:addcredential"
    #classes = ("ajax-modal", "btn-edit")
    #policy_rules = (("credential", "add_credential"),)
    name = "credential"
    verbose_name = _("AddCredential")
    url = "horizon:project:images:images:addcredential"
    classes = ("ajax-modal", "btn-edit")
    policy_rules = (("credential", "add_credential"),)

    def allowed(self,request,repo=None):
        result = glint.get_glint_url_and_token(request) 
        #attr=dir(repo)
        #print "Should credential be Add and Edit %s repo %s attr:"%(result,repo.id)
        data_json = requests.post("%shascredential/"%result['url'],data={"CK_TYPE":"ONE","SITE_ID":repo.id,"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
        #print "Allow the cred button says %s"%data_json
        data_dict = json.loads(data_json)
        #print "Allow the cred button says %s"%data_dict
        if data_dict['result'] is True:
            self.verbose_name = _("EditCredential")
            self.url = "horizon:project:images:images:editcredential"
        return True
    
class DeleteCredential(tables.Action):
    verbose_name = _("Delete Credential")
    attrs=None
    name="delcred"
    #preempt=None
    #method=None
    #handle = 'single'

    def _allowed(self, request, cred=None):
        try:
            # Protected images can not be deleted.
            print("check if delete Cred is allowed %s"%cred)
            if cred is None:
                print "Cred is None, Dont show delete credential"
                return False
            #if site and site.protected:
            #    return False
            #if site:
            #    return site.owner == request.user.tenant_id
            # Return True to allow table-level bulk delete action to appear.
            result = glint.get_glint_url_and_token(request) 
            data_json = requests.post("%shascredential/"%result['url'],data={"CK_TYPE":"ONE","SITE_ID":cred.id,"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
            #print "Allow the cred button says %s"%data_json
            data_dict = json.loads(data_json)
            #print "Allow the cred button says %s"%data_dict
            if data_dict['result'] is True:
                #self.verbose_name = _("EditCredential")
                #print "Show Delete Credential"
                return True
            #print "Don't Show Delete Credential"
            return False
        except:
            print "Esception occured on det if del cred is visible dont show del credential"
            return False

      
    def handle(self,table, request, obj_id):
        #print "Handle this Biasth %s %s"%(obj_id,obj_id[0])
        result = glint.get_glint_url_and_token(request) 
        data_json = requests.post("%sdeletecredential/"%result['url'],data={"SITE_ID":obj_id[0],"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
        #data_obj = json.loads(data_json)
        #print "hanlde this Received back %s"%data_json
        
    #def action(self, request, obj_id):
    #    print("Update -sing- Cred %s"%obj_id)
    #    result = glint.get_glint_url_and_token(request) 
    #    data_json = requests.post("%sdeletecredential/"%result['url'],data={"SITE_ID":obj_id[0],"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
    #    #data_obj = json.loads(data_json)
    #    print "Received back %s"%data_json

    
class DeleteSite(tables.DeleteAction):
    data_type_singular = _("Repository")
    data_type_plural = _("Repository")
    policy_rules = (("site", "delete_site"),)

    def allowed(self, request, site=None):
        try:
            # Protected images can not be deleted.
            #print("check if delete site is allowed %s"%site)
            if site is None:
                #print "Delete  site is none, but show Delete Site"
                return False
            #if site and site.protected:
            #    return False
            #if site:
            #    return site.owner == request.user.tenant_id
            # Return True to allow table-level bulk delete action to appear.
            result = glint.get_glint_url_and_token(request) 
            data_json = requests.post("%shascredential/"%result['url'],data={"CK_TYPE":"ALL","SITE_ID":site.id,"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
            #print "Allow the site button says %s"%data_json
            data_dict = json.loads(data_json)
            #print "Allow the site button says %s"%data_dict
            if data_dict['result'] is True:
                #self.verbose_name = _("EditCredential")
                #print "Don't Show Delete Site Cause Cred exists"
                return False
            #print "Show Delete Site"
            return True
        except:
            #print "Exception occured on del stie is avail on site %s"%site
            return False

    def delete(self, request, obj_id):
        #print("delete Site %s"%obj_id)
        result = glint.get_glint_url_and_token(request) 
        data_json = requests.post("%sdeletesite/"%result['url'],data={"SITE_ID":obj_id,"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
        #data_obj = json.loads(data_json)
        print "Received back %s"%data_json  


class CreateSite(tables.LinkAction):
    name = "create"
    verbose_name = _("Add Repository")
    url = "horizon:project:images:images:createsite"
    classes = ("ajax-modal", "btn-create")
    policy_rules = (("site", "create_site"),)


class EditImage(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:project:images:images:update"
    classes = ("ajax-modal", "btn-edit")
    policy_rules = (("image", "modify_image"),)

    def allowed(self, request, image=None):
        #if image:
        ##    return image.status in ("active",) and \
        #        image.owner == request.user.tenant_id
        # We don't have bulk editing, so if there isn't an image that's
        # authorized, don't allow the action.
        return True


class CreateVolumeFromImage(tables.LinkAction):
    name = "create_volume_from_image"
    verbose_name = _("Create Volume")
    url = "horizon:project:volumes:volumes:create"
    classes = ("ajax-modal", "btn-camera")
    policy_rules = (("volume", "volume:create"),)

    def get_link_url(self, datum):
        base_url = reverse(self.url)
        params = urlencode({"image_id": self.table.get_object_id(datum)})
        return "?".join([base_url, params])

    def allowed(self, request, image=None):
        if (image and image.container_format not in NOT_LAUNCHABLE_FORMATS
                and base.is_service_enabled(request, 'volume')):
            return image.status == "active"
        return False


def filter_tenants():
    return getattr(settings, 'IMAGES_LIST_FILTER_TENANTS', [])


@memoized
def filter_tenant_ids():
    return map(lambda ft: ft['tenant'], filter_tenants())


class OwnerFilter(tables.FixedFilterAction):
    def get_fixed_buttons(self):
        def make_dict(text, tenant, icon):
            return dict(text=text, value=tenant, icon=icon)

        buttons = [make_dict(_('Project'), 'project', 'icon-home')]
        for button_dict in filter_tenants():
            new_dict = button_dict.copy()
            new_dict['value'] = new_dict['tenant']
            buttons.append(new_dict)
        buttons.append(make_dict(_('Shared with Me'), 'shared', 'icon-share'))
        buttons.append(make_dict(_('Public'), 'public', 'icon-fire'))
        return buttons

    def categorize(self, table, images):
        user_tenant_id = table.request.user.tenant_id
        tenants = defaultdict(list)
        for im in images:
            categories = get_image_categories(im, user_tenant_id)
            for category in categories:
                tenants[category].append(im)
        return tenants


def get_image_categories(im, user_tenant_id):
    categories = []
    if im.is_public:
        categories.append('public')
    if im.owner == user_tenant_id:
        categories.append('project')
    elif im.owner in filter_tenant_ids():
        categories.append(im.owner)
    elif not im.is_public:
        categories.append('shared')
    return categories


def get_image_name(image):
    return getattr(image, "name", None) or image.id


def get_site_url(site):
    return site.url

def get_site_authport(site):
    return site.authport

def get_site_type(site):
    return site.type

def get_site_name(site):
    #print "site data %s"%site.site_name
    #site_index++
    return site.site_name

def get_image_type(image):
    return getattr(image, "properties", {}).get("image_type", "image")


def get_format(image):
    format = getattr(image, "disk_format", "")
    # The "container_format" attribute can actually be set to None,
    # which will raise an error if you call upper() on it.
    if format is not None:
        return format.upper()

class UpdateSiteRow(tables.Row):
    ajax = True

    def get_data(self, request, site_id):
        #image = api.glance.image_get(request, image_id)
        #print "get site %s"%site_id
        site = site_data[site_id]
        #site_id=site_id+1
        return site

    def load_cells(self, site=None):
        #print "loading %s"%image
        super(UpdateSiteRow, self).load_cells(site)
        # Tag the row with the image category for client-side filtering.
        site = self.datum
       # print "load data"
        #my_tenant_id = self.table.request.user.tenant_id
        #image_categories = get_image_categories(image, my_tenant_id)
        #for category in image_categories:
        #    self.classes.append('category-' + category)

class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, image_id):
        image = api.glance.image_get(request, image_id)
        return image

    def load_cells(self, image=None):
        super(UpdateRow, self).load_cells(image)
        # Tag the row with the image category for client-side filtering.
        image = self.datum
        my_tenant_id = self.table.request.user.tenant_id
        image_categories = get_image_categories(image, my_tenant_id)
        for category in image_categories:
            self.classes.append('category-' + category)




class SitesTable(tables.DataTable):
    #STATUS_CHOICES = (
    #    ("active", True),
    #    ("saving", None),
    #    ("queued", None),
    #    ("pending_delete", None),
    #    ("killed", False),
    #    ("deleted", False),
    #)
    name = tables.Column(get_site_name, verbose_name=_("Name"))
    site_url = tables.Column(get_site_url, verbose_name=_("Identity Service Endpoint URL"))
    #auth_port = tables.Column(get_site_authport, verbose_name=_("Auth Port"))
    site_type = tables.Column(get_site_type, verbose_name=_("Cloud Type"))
    #status = tables.Column("status",
    #                       filters=(filters.title,),
    #                       verbose_name=_("Status"),
    #                       status=True,
    #                       status_choices=STATUS_CHOICES)
    #public = tables.Column("is_public",
    #                       verbose_name=_("Public"),
    #                       empty_value=False,
    #                       filters=(filters.yesno, filters.capfirst))
    #protected = tables.Column("protected",
    #                          verbose_name=_("Protected"),
    #                          empty_value=False,
    #                          filters=(filters.yesno, filters.capfirst))
    

    class Meta:
        name = "sites"
        row_class = UpdateSiteRow
        #status_columns = ["status"]
        verbose_name = _("Repositories")
        table_actions = ( CreateSite, DeleteSite )
        row_actions = ( AddCredential,DeleteSite, DeleteCredential )
        pagination_param = "site_marker"
