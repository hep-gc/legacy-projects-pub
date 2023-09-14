'''
Created on Apr 3, 2014

@author: rd
'''
import unittest
import ec2_api_tools.SpotPriceServiceClient as spc

import datetime as dt
import dateutil.parser


class TestCurrentSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        result=spc.get_current_spot_price(["Linux/UNIX"], ["t1.micro"], ["us-west-2"], [], "none", "json")
        assert isinstance(result[0]['price'],float)
        pass

class TestListAllSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        result=spc.list_all_spot_price(["Linux/UNIX"], ["t1.micro"], ["us-west-2"], [], "none", "json",8)
        assert isinstance(result[0]['price'],float)
        pass
    
class TestPeriodicSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        stop_date = dt.datetime.now().isoformat()
        start_date = (dt.datetime.now()-dt.timedelta(hours=1680)).isoformat()
        result=spc.get_periodic_spot_price(["Linux/UNIX"], ["t1.micro"], ["us-west-2"], ["us-west-2a"], "none", "json",1,168, start_date , stop_date)
        print("len %s"%len(result))
        assert isinstance(result[0]['price'],float)
        assert len(result)==10 or len(result)==9 or len(result)==11
        pass
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()