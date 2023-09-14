'''
Created on Apr 3, 2014

@author: rd
'''
from pprint import pprint

def create_request(req_type,filter_type,response_type,other_args,args):
    if req_type == 'current_spot_price' or req_type == 'list_all_spot_price' or req_type == 'periodic_spot_price':
        msg = {}
        msg['filter_type']=filter_type
        msg['response_type']=response_type
        msg['request']=req_type
        msg['other_args']=other_args
        msg['request_args']=args
        return msg
       
        