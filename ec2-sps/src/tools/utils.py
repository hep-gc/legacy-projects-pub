'''
Created on Apr 1, 2014

@author: rd
'''
from pprint import pprint
import json

def filter_response(json_resp, filter_type):
    #pprint("filter response %s"%filter_type)
    if filter_type == "none":
        #pprint("no filtering required")
        return json_resp
    elif filter_type == "highest":
        highest=0.0
        highest_idx=-1;
        remove_idx=[]
        #pprint("find highest required")
        for idx,entry in enumerate(json_resp):
            #pprint("found cost %s %s"%(entry['price'],idx))
            if entry['price'] <= highest:
                #pprint("removing %i"%idx)
                #del json_resp[idx]
                remove_idx.append(idx)
            else:
                #pprint("new high %s"%entry['price'])
                
                remove_idx.append(idx)
                #del json_resp[highest_idx]
                highest_idx=idx
                highest=entry['price']
        #numpy.delete()
        #np.delete(json_resp,remove_idx)
        if highest_idx != -1:
            del remove_idx[highest_idx]
        while len(remove_idx)>0:
            idx = remove_idx.pop()
            #pprint("REM %s"%idx)
            del json_resp[idx]
            
            
        #pprint("idx %s"%remove_idx)
        return json_resp
    elif filter_type == "average":
        pprint("find average")    
        total=0.0
        idx=0
        remove_idx=[]
        #pprint("find highest required")
        for idx,entry in enumerate(json_resp):
            #pprint("found cost %s %s"%(entry['price'],idx))
            total=total+entry['price']
            remove_idx.append(idx)
        average=total/(1+idx)
        while len(remove_idx)>0:
            idx = remove_idx.pop()
            #pprint("REM %s"%idx)
            del json_resp[idx]
        json_str = '{"zone":"","image_type":"","timestamp":"","region":"","instance_type":"","price":%s}'%average
        pprint(json_str)
        json_obj = json.loads(json_str)
        json_resp.append(json_obj)   
            
        #pprint("idx %s"%remove_idx)
        return json_resp
