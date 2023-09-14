'''
Created on Mar 10, 2014

@author: rd
'''
from django.conf.urls import patterns, url

from ec2_spot_price_monitor import views


urlpatterns = patterns('',
                      url(r'^$', views.index, name='index'),
                      url(r'^spot_price/', views.request_spot_price, name='request_spot_price'),
)

views.init_spot_price_service()