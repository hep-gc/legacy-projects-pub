# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

"""
Views for managing images.
"""
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized
 
from openstack_dashboard import api

from openstack_dashboard.dashboards.project.images.images \
    import forms as project_forms 
from openstack_dashboard.dashboards.project.images.images \
    import tabs as project_tabs

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openstack_dashboard.api import glint
import requests,json

@csrf_exempt
def save(request):
    #print "redirect save request to glint %s"%request.POST['jsonMsg']
    result = glint.get_glint_url_and_token(request) 
    data_json = requests.post("%ssave/"%result['url'],data={"jsonMsg":request.POST['jsonMsg'],"USER_ID":request.user,"USER_TOKEN":"%s"%result['token'],"USER_TENANT":request.user.token.tenant['name']},cookies=None).text
    #print "received %s "%data_json
    return HttpResponse("%s"%data_json)

class EditCredentialView(forms.ModalFormView):
    form_class = project_forms.AddCredentialForm 
    template_name = 'project/images/credentials/edit.html'
    context_object_name = 'credential'
    success_url = reverse_lazy("horizon:project:images:index")
    
    @memoized.memoized_method
    def get_object(self):
        #print "Get Credentials Objects"
        result = glint.get_glint_url_and_token(self.request) 
        obj = {}
        obj['site_id']=self.kwargs['site_id']
        obj['USER_TOKEN']=result['token']
        obj['USER_ID']=str(self.request.user)
        obj['USER_TENANT']=self.request.user.token.tenant['name']
        
        data_json = requests.post("%sgetcredential/"%result['url'],data={"CK_TYPE":"ONE","SITE_ID":obj['site_id'],"USER_ID":obj['USER_ID'],"USER_TOKEN":"%s"%result['token'],"USER_TENANT":obj['USER_TENANT']},cookies=None).text
        #print "Get Credentials returned %s"%data_json
        obj['REMOTE_SITE_CREDS']=data_json
        
        return obj
        #try:
        #    return api.glance.image_get(self.request, self.kwargs['image_id'])
        #except Exception:
        #    msg = _('Unable to retrieve image.')
        #    url = reverse('horizon:project:images:index')
        #    exceptions.handle(self.request, msg, redirect=url)

    def get_context_data(self, **kwargs):
        #print "get CredentialView Context Data"
        context = super(EditCredentialView, self).get_context_data(**kwargs)
        #print "Sontext STR %s"%context
        #context['form'].fields['tenent'].initial=context
        context['credential'] = self.get_object()
        #print "form str %s"%context['credential']['REMOTE_SITE_CREDS']
        json_obj = json.loads(context['credential']['REMOTE_SITE_CREDS'])
        #print "json obj is %s"%json_obj
        context['form'].fields['tenent'].initial=json_obj['tenant']
        context['form'].fields['username'].initial=json_obj['cred_id']
        return context

    def get_initial(self):
        #print "INIT SITE INFO %s"%self.get_object()
        return self.get_object()
        #image = self.get_object()
        #properties = getattr(image, 'properties', {})
        #return {'image_id': self.kwargs['image_id'],
        #        'name': getattr(image, 'name', None) or image.id,
        #        'description': properties.get('description', ''),
        #        'kernel': properties.get('kernel_id', ''),
        #       'ramdisk': properties.get('ramdisk_id', ''),
        #        'architecture': properties.get('architecture', ''),
        #        'disk_format': getattr(image, 'disk_format', None),
        #        'public': getattr(image, 'is_public', None),
        #        'protected': getattr(image, 'protected', None)}

    
    
class AddCredentialView(forms.ModalFormView):
    form_class = project_forms.AddCredentialForm 
    template_name = 'project/images/credentials/create.html'
    context_object_name = 'credential'
    success_url = reverse_lazy("horizon:project:images:index")
    
    @memoized.memoized_method
    def get_object(self):
        print "Get Credentials Object"
        obj = {}
        obj['site_id']=self.kwargs['site_id']
        return obj
        #try:
        #    return api.glance.image_get(self.request, self.kwargs['image_id'])
        #except Exception:
        #    msg = _('Unable to retrieve image.')
        #    url = reverse('horizon:project:images:index')
        #    exceptions.handle(self.request, msg, redirect=url)

    def get_context_data(self, **kwargs):
        print "get CredentialView Context Data"
        context = super(AddCredentialView, self).get_context_data(**kwargs)
        print "context str %s"%context
        context['credential'] = self.get_object()
        print "new context str %s"%context
        return context

    def get_initial(self):
        print "init site info %s"%self.get_object()
        return self.get_object()
        #image = self.get_object()
        #properties = getattr(image, 'properties', {})
        #return {'image_id': self.kwargs['image_id'],
        #        'name': getattr(image, 'name', None) or image.id,
        #        'description': properties.get('description', ''),
        #        'kernel': properties.get('kernel_id', ''),
        #       'ramdisk': properties.get('ramdisk_id', ''),
        #        'architecture': properties.get('architecture', ''),
        #        'disk_format': getattr(image, 'disk_format', None),
        #        'public': getattr(image, 'is_public', None),
        #        'protected': getattr(image, 'protected', None)}

    
class CreateSiteView(forms.ModalFormView):
    form_class = project_forms.CreateSiteForm
    template_name = 'project/images/sites/create.html'
    context_object_name = 'site'
    success_url = reverse_lazy("horizon:project:images:index")

class CreateView(forms.ModalFormView):
    form_class = project_forms.CreateImageForm
    template_name = 'project/images/images/create.html'
    context_object_name = 'image'
    success_url = reverse_lazy("horizon:project:images:index")


class UpdateView(forms.ModalFormView):
    form_class = project_forms.UpdateImageForm
    template_name = 'project/images/images/update.html'
    success_url = reverse_lazy("horizon:project:images:index")

    @memoized.memoized_method
    def get_object(self):
        try:
            return api.glance.image_get(self.request, self.kwargs['image_id'])
        except Exception:
            msg = _('Unable to retrieve image.')
            url = reverse('horizon:project:images:index')
            exceptions.handle(self.request, msg, redirect=url)

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['image'] = self.get_object()
        return context

    def get_initial(self):
        image = self.get_object()
        properties = getattr(image, 'properties', {})
        return {'image_id': self.kwargs['image_id'],
                'name': getattr(image, 'name', None) or image.id,
                'description': properties.get('description', ''),
                'kernel': properties.get('kernel_id', ''),
                'ramdisk': properties.get('ramdisk_id', ''),
                'architecture': properties.get('architecture', ''),
                'disk_format': getattr(image, 'disk_format', None),
                'public': getattr(image, 'is_public', None),
                'protected': getattr(image, 'protected', None)}


class DetailView(tabs.TabView):
    tab_group_class = project_tabs.ImageDetailTabs
    template_name = 'project/images/images/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["image"] = self.get_data()
        return context

    @memoized.memoized_method
    def get_data(self):
        try:
            return api.glance.image_get(self.request, self.kwargs['image_id'])
        except Exception:
            url = reverse('horizon:project:images:index')
            exceptions.handle(self.request,
                              _('Unable to retrieve image details.'),
                              redirect=url)

    def get_tabs(self, request, *args, **kwargs):
        image = self.get_data()
        return self.tab_group_class(request, image=image, **kwargs)
