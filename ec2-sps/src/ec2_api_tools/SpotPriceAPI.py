'''
Created on Mar 31, 2014

@author: rd
'''
import spot_price_api as spi
from django.utils.translation import ugettext_lazy as _
import sys
import datetime as dt
from pprint import pprint 

WINDOWS,SUSE,LINUX_UNIX = 'Windows','SUSE Linux','Linux/UNIX'

T1_M,M1_S,M1_M,M1_L,M1_X ='t1.micro','m1.small','m1.medium','m1.large','m1.xlarge'
M2_X,M2_2X,M2_4X,M3_M,M3_L,M3_X,M3_2X = 'm2.xlarge','m2.2xlarge','m2.4xlarge','m3.medium','m3.large','m3.xlarge','m3.2xlarge'
C1_M,C1_X,C3_X,C3_2X,C3_4X,C3_8X = 'c1.medium','c1.xlarge','c3.xlarge','c3.2xlarge','c3.4xlarge','c3.8xlarge'
CC2_8X,CR1_8X,G2_2X,HI1_4X = 'cc2.8xlarge','cr1.8xlarge','g2.2xlarge','hi1.4xlarge'

OREGON = 'us-west-2'
OREGONA,OREGONB,OREGONC = 'us-west-2a','us-west-2b','us-west-2c'

def get_current_spot_price(image,instance,region,zone):
    pprint("get current spot price %s %s %s  %s"%(image,instance,region,zone ))
    #create json message 
    json_req = {}
    json_req['request_args'] = []
    
    img_type = {}
    img_type['ImageTypes'] = []
    img_type['ImageTypes'].append(image)
    json_req['request_args'].append(img_type)
    
    inst_type = {}
    inst_type['InstanceTypes'] = []
    inst_type['InstanceTypes'].append(instance)
    json_req['request_args'].append(inst_type)
    
    reg_type = {}
    reg_type['Regions'] = []
    reg_type['Regions'].append(region)
    json_req['request_args'].append(reg_type)
    
    zone_type = {}
    zone_type['ZONES'] = []
    zone_type['ZONES'].append(zone)
    json_req['request_args'].append(zone_type)
    
    json_req['start_time'] = dt.datetime.now().isoformat()
    json_req['end_time'] = dt.datetime.now().isoformat()
    
    pprint(json_req)
    json_response_data = spi.get_current_spot_price(json_req)
    pprint(json_response_data)
    return json_response_data[0]['price']

def main(argv):
    pprint("main this")
    pprint("price %s"%get_current_spot_price(LINUX_UNIX,M3_M,OREGON,OREGONA))
    pass

if __name__ == "__main__":
    main(sys.argv)