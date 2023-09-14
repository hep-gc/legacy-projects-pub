from django.db import models

from django.utils.translation import ugettext_lazy as _
from pprint import pprint

class InstanceType(models.Model):
    T1_M,M1_S,M1_M,M1_L,M1_X ='t1.micro','m1.small','m1.medium','m1.large','m1.xlarge'
    M2_X,M2_2X,M2_4X,M3_M,M3_L,M3_X,M3_2X = 'm2.xlarge','m2.2xlarge','m2.4xlarge','m3.medium','m3.large','m3.xlarge','m3.2xlarge'
    C1_M,C1_X,C3_X,C3_2X,C3_4X,C3_8X = 'c1.medium','c1.xlarge','c3.xlarge','c3.2xlarge','c3.4xlarge','c3.8xlarge'
    CC2_8X,CR1_8X,G2_2X,HI1_4X = 'cc2.8xlarge','cr1.8xlarge','g2.2xlarge','hi1.4xlarge'
    INSTANCETYPE = ( (T1_M,_(T1_M)),(M1_S,_(M1_S)),(M1_M,_(M1_M)),(M1_L,_(M1_L)),(M1_X,_(M1_X)) ,
                     (M2_X,_(M2_X)),(M2_2X,_(M2_2X)),(M2_4X,_(M2_4X)),(M3_M,_(M3_M)),(M3_L,_(M3_L)),(M3_X,_(M3_X)),(M3_2X,_(M3_2X)),
                      (C1_M,_(C1_M)),(C1_X,_(C1_X)),(C3_X,_(C3_X)),(C3_2X,_(C3_2X)),(C3_4X,_(C3_4X)),(C3_8X,_(C3_8X)),
                      (CC2_8X,_(CC2_8X)),(CR1_8X,_(CR1_8X)),(G2_2X,_(G2_2X)),(HI1_4X,_(HI1_4X)) )
    
    instance_type = models.CharField(max_length=200,choices=INSTANCETYPE,default=M3_M)
    ARCHS =(('BIT64','64 Bit'),('BIT32','32 Bit'))
    proc_arch = models.CharField(max_length=200,choices=ARCHS,default='BIT64')
    v_cpu = models.IntegerField(default=1,choices=((1,"1"),(2,"2"),(4,"4"),(8,"8"),(16,"16"),(32,"32"),(64,"64")))
    memory = models.FloatField(default=3.75)
    inst_storage = models.CharField(max_length=200,default="4 GB SSD")
    net_perf = models.CharField(max_length=200,default="M",choices=( ("M","Moderate"),("H","High"),("L","Low"),("VL","Very Low") ))
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.instance_type

class Region(models.Model):
    US_WEST_OREGON,US_WEST_CAL,US_EAST_VIR,EU_IRE,ASIA_PAC_SIG,ASIA_PAC_TOKYO,ASIA_PAC_SYDNEY,SOUTH_AM_SAN_PAULO='Oregon (us-west-2)','California (us-west-2)','Virginia (us-east-1)','Ireland (eu-west-1)','Singapore (ap-southeast-1)','Tokyo (ap-northeast-1)','Sydney (ap-southeast-2)','San Paulo (sa-east-1)'
    SITE = ( ((US_WEST_OREGON),_(US_WEST_OREGON)),((US_WEST_CAL),_(US_WEST_CAL)),((US_EAST_VIR),_(US_EAST_VIR)),((EU_IRE),_(EU_IRE)),((ASIA_PAC_SIG),_(ASIA_PAC_SIG)),((ASIA_PAC_TOKYO),_(ASIA_PAC_TOKYO)),((ASIA_PAC_SYDNEY),_(ASIA_PAC_SYDNEY)),((SOUTH_AM_SAN_PAULO),_(SOUTH_AM_SAN_PAULO)) )
    
    site = models.CharField(max_length=200,choices=SITE,default=US_WEST_OREGON)
    
    ZONE_A,ZONE_B,ZONE_C,ZONE_D='a','b','c','d'
    ZONE = ( ((ZONE_A),_(ZONE_A)),((ZONE_B),_(ZONE_B)),((ZONE_C),_(ZONE_C)),((ZONE_D),_(ZONE_D)) )
    
    zone = models.CharField(max_length=200,choices=ZONE,default=ZONE_A)
    
    def __str__(self):
        return ("%s%s" %(self.site,self.zone))

class ImageType(models.Model):
    WINDOWS,SUSE,LINUX_UNIX = 'Windows','SUSE Linux','Linux/UNIX'
    IMG_TYPE = ( (WINDOWS,_(WINDOWS)),(SUSE,_(SUSE)),(LINUX_UNIX,_(LINUX_UNIX)) )
    
    image_type = models.CharField(max_length=200,choices=IMG_TYPE,default=LINUX_UNIX)
    image_description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.image_type
    
class SpotPrice(models.Model):
    type = models.ForeignKey(InstanceType)
    region = models.ForeignKey(Region)
    date = models.DateField()
    time = models.TimeField()
    description = models.ForeignKey(ImageType)
    cost = models.DecimalField(decimal_places=5,max_digits=6)
    
    def __str__(self):
        return ("%s %s "%(self.type,self.region))
    

    
    
    