"""@package ec2_api_tools
Documentation

Create by rd
April 2, 2014
"""
import sys,json,logging, requests, json_factory


URL = ""

def _show_help():
    """Documentation for a function.
    basic help function with examples
    """
    print 'usage: python SpotPriceServiceAPI -[h rt jt jo je jp it nt r z ft df] <NAME/VALUE>'
    print "  -h   :usage"
    print("  -rt  :request type NAME needs to be one of 'current_spot_price','list_all_spot_price','periodic_spot_price'")
    print("  -jt  :spot cost search start time and ISO Date String i.e. '2014-03-02T20:09:07.157Z' ")
    print("  -jo  :spot cost search stop time and ISO Date String i.e. '2014-03-02T20:09:07.157Z' - later than or equal to job start time")
    print("  -je  :job execution time in hours i.e. '7' ")
    print("  -jp  :periodic time - in hours- i.e. '168' - is one week ")
    print("  -it  :image type needs to be one of 'Linux/UNIX','SUSE Linux','Windows' ")
    print("  -nt  :instance type needs to be one of 't1.micro','m3.medium','c3.2xlarge','m3.large','cc2.8xlarge','m1.medium' ")
    print("  -r   :region type needs to be one or more of 'us-east-1','us-west-1','us-west-2','eu-west-1','ap-northeast-1','ap-southeast-1','ap-southeast-2','sa-east-1' ")
    print("  -z   :zone type needs to be one or more of region+'a','b','c','d' i.e., 'us-west-2a','us-west-2b' ")
    print("  -ft  :filter type needs to be one of 'none','average','highest' ")
    print("  -df  :data filter needs to be one of 'json','html' ")
    print("")
    print("")
    print("Example Usage")
    print("--------------")
    print("To determine current spot price of an m3.medium vm type in region us-west-2 and return all results in json format")
    print("")
    print("blogins@machine:~$ python SpotPriceServiceAPI.py -rt current_spot_price -it Linux/UNIX -nt m3.medium -r us-west-2 -ft none -df json ")
    print("")
    print("")
    print("To determine current spot price of 2 vm types in 2 regions and return the average result in html format")
    print("")
    print("blogins@machine:~$ python SpotPriceServiceAPI.py -rt current_spot_price -it Linux/UNIX -nt t1.micro m1.medium -r us-west-2 us-west-1 -ft average -df html ")
    print("")
    print("")
    print("To determine periodic (over past 3 months, every Monday from 8:09pm till Tuesday 4:09am = 8 hour job) spot price of an m3.medium vm type in region us-west-2 and return all results in json format")
    print("")
    print("blogins@machine:~$ python SpotPriceServiceAPI.py -rt periodic_spot_price -it Linux/UNIX -jt 2014-01-02T20:09:07.157Z -jo 2014-03-02T20:09:07.157Z -je 8 -jp 168 -nt m3.medium -r us-west-2 -ft none -df json ")
    print("")
    print("")
    
def _get_arg(argv,tag):
    """ get_arg
    argv @array of commandline arguments
    tag  $string of tag to parse for
    """
    state= 0;
    ret_args=[]
    for arg in argv:
        if state == 1:
            if arg.find('-') == 0:
                break;
            ret_args.append(arg)
        if arg == tag:
            state =1
    return ret_args;        

def _generate_args(args,argv):
    """generate_args
    args @array empty
    argv @array of command line arguments
    """
    args.append( {"ImageTypes":_get_arg(argv,'-it')} )  
    args.append({"InstanceTypes":  _get_arg(argv,'-nt') })
    args.append({"Regions": _get_arg(argv,'-r')})
    args.append({"ZONES": _get_arg(argv,'-z') })
   
    return [args,_get_arg(argv,'-ft')[0],_get_arg(argv,'-df')[0]]

def get_current_spot_price(image_type,instance_type,regions,zones,filter_type,response_type):
    """API function
    image_type $string see help -h 
    instance_type $string see help -h 
    regions @array of strings see help -h 
    zones @array of strings see help -h 
    filter_type $string see help -h 
    response_type $string see help -h 
    """
    args = []
    args.append( {"ImageTypes":image_type} )  
    args.append({"InstanceTypes":  instance_type })
    args.append({"Regions": regions})
    args.append({"ZONES": zones })
    json_req = json_factory.create_request('current_spot_price',filter_type,response_type,{},args)
    json_response_data = json.loads(requests.post(URL,data={"jsonMsg":json.dumps(json_req)},cookies=None).text)
    logging.debug(json_req)
    print(json_response_data['response_data'])
    return json_response_data['response_data']
    
def list_all_spot_price(image_type,instance_type,regions,zones,filter_type,response_type,job_exe_time):
    """API function
    image_type $string see help -h 
    instance_type $string see help -h 
    regions @array of strings see help -h 
    zones @array of strings see help -h 
    filter_type $string see help -h 
    response_type $string see help -h 
    job_exe_time integer see help -h
    """
    args = []
    args.append( {"ImageTypes":image_type} )  
    args.append({"InstanceTypes":  instance_type })
    args.append({"Regions": regions})
    args.append({"ZONES": zones })
    other_args={}
    other_args['job_exe_time']=job_exe_time
    json_req = json_factory.create_request('list_all_spot_price',filter_type,response_type,other_args,args)
    json_response_data = json.loads(requests.post(URL,data={"jsonMsg":json.dumps(json_req)},cookies=None).text)
    logging.debug(json_req)
    print(json_response_data)   
    return json_response_data['response_data']     
    
def get_periodic_spot_price(image_type,instance_type,regions,zones,filter_type,response_type,job_exec_time,job_period_time,job_start_time,job_stop_time):
    """API function
    image_type $string see help -h 
    instance_type $string see help -h 
    regions @array of strings see help -h 
    zones @array of strings see help -h 
    filter_type $string see help -h 
    response_type $string see help -h 
    job_exec_time integer see help -h
    job_period_time integer see help -h
    job_start_time ISO 9801 DateTime string see help -h
    job_stop_time ISO 9801 DateTime string see help -h
    """
    args = []
    args.append( {"ImageTypes":image_type} )  
    args.append({"InstanceTypes":  instance_type })
    args.append({"Regions": regions})
    args.append({"ZONES": zones })
    other_args={}
    other_args['job_exec_time']=job_exec_time
    other_args['job_period_time']=job_period_time
    other_args['job_start_time']=job_start_time
    other_args['job_stop_time']=job_stop_time
    json_req = json_factory.create_request('periodic_spot_price',filter_type,response_type,other_args,args)
    json_response_data = json.loads(requests.post(URL,data={"jsonMsg":json.dumps(json_req)},cookies=None).text)
    logging.debug(json_req)
    print(json_response_data)
    return json_response_data['response_data']

def _main(argv): 
    """main function
    argv @array of command line arguments
    """
    state = 0
    req_type = ''
    for arg in argv:
        if arg == '-h':
            _show_help()
            sys.exit(0)
        if arg == '-rt':
            state = 1
        else:
            if state == 1:
                req_type = arg
            state = 0
    logging.info("Request Type %s"%req_type)
    if req_type == 'current_spot_price':
        [args,filter_type,response_type]=_generate_args([],argv)
        json_req = json_factory.create_request(req_type,filter_type,response_type,{},args)
        json_response_data = json.loads(requests.post(URL,data={"jsonMsg":json.dumps(json_req)},cookies=None).text)
        logging.debug(json_req)
        print(json_response_data['response_data'])
    elif req_type == 'list_all_spot_price':
        [args,filter_type,response_type]=_generate_args([],argv)
        other_args={}
        other_args['job_exe_time']=int(_get_arg(argv,'-je')[0])
        json_req = json_factory.create_request(req_type,filter_type,response_type,other_args,args)
        json_response_data = json.loads(requests.post(URL,data={"jsonMsg":json.dumps(json_req)},cookies=None).text)
        logging.debug(json_req)
        print(json_response_data)        
    elif req_type == 'periodic_spot_price':
        [args,filter_type,response_type]=_generate_args([],argv)
        other_args={}
        other_args['job_exec_time']=int(_get_arg(argv,'-je')[0])
        other_args['job_period_time']=int(_get_arg(argv,'-jp')[0])
        other_args['job_start_time']=_get_arg(argv,'-jt')[0]
        other_args['job_stop_time']=_get_arg(argv,'-jo')[0]
        json_req = json_factory.create_request(req_type,filter_type,response_type,other_args,args)
        json_response_data = json.loads(requests.post(URL,data={"jsonMsg":json.dumps(json_req)},cookies=None).text)
        logging.debug(json_req)
        print(json_response_data)
        
    pass

if __name__ == "__main__":
    cmd_str = sys.argv[0].replace("SpotPriceServiceAPI.py","spot_price_api.cfg")
    config_file = open(cmd_str)
    cfg_file = ""
    for line in config_file:
        cfg_file = "%s%s"%(cfg_file,line)
    cfg_obj = json.loads(cfg_file)
    URL = cfg_obj['URL']
    
    logging.basicConfig(filename=cfg_obj['LOG_FILE_NAME'],level=eval(cfg_obj['LOGGING_LEVEL']),format='%(asctime)s %(message)s')
    
    config_file.close()
    _main(sys.argv)