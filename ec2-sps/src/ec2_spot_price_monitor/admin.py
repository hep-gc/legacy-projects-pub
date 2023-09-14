'''
Created on Mar 10, 2014

@author: rd
'''
from django.contrib import admin
from ec2_spot_price_monitor.models import SpotPrice,InstanceType,ImageType,Region

class SpotPriceAdmin(admin.ModelAdmin):
    list_display = ('type','region','date','time','cost')
    list_filter = ('type','region','date','time','cost')
    
class InstanceTypeAdmin(admin.ModelAdmin):
    list_display = ('instance_type','proc_arch','v_cpu','memory','inst_storage','net_perf', 'description')
    list_filter = ('instance_type','proc_arch','v_cpu','memory','inst_storage','net_perf','description')
    
class ImageTypeAdmin(admin.ModelAdmin):
    list_display = ('image_type','image_description')
    list_filter = ('image_type','image_description')
    
class RegionAdmin(admin.ModelAdmin):
    list_display = ('site','zone')
    list_filter = ('site','zone')

admin.site.register(InstanceType,InstanceTypeAdmin)
admin.site.register(ImageType,ImageTypeAdmin)
admin.site.register(Region,RegionAdmin)
admin.site.register(SpotPrice,SpotPriceAdmin)