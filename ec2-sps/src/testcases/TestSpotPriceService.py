'''
Created on Apr 3, 2014

@author: rd
'''
#from ec2_api_tools import test.test
import client.SpotPriceServiceClient as spc

import datetime as dt

import unittest

class TestUSW2HighestPeriodicSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        start_date = (dt.datetime.now()-dt.timedelta(hours=1681)).isoformat()
        price=spc.get_highest_us_west_2_periodic_spot_price("m1.medium",24,start_date,168)
        print ("Highest Weekly m1.medium price is %s over past 10 weeks"%price)
        assert isinstance(price,float)
        pass

class TestUSW2AveragePeriodicSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        start_date = (dt.datetime.now()-dt.timedelta(hours=1704)).isoformat()
        price=spc.get_average_us_west_2_periodic_spot_price("m1.medium",24,start_date,168)
        print ("Average Weekly m1.medium price is %s over past 10 weeks"%price)
        assert isinstance(price,float)
        pass

class TestUSW2HighestDurationSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        price=spc.get_highest_us_west_2_spot_price("m1.medium",24)
        print ("Highest m1.medium price is %s over past 24 hour duration"%price)
        assert isinstance(price,float)
        pass
    
class TestUSW2AverageDurationSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        price=spc.get_average_us_west_2_spot_price("m1.medium",24)
        print ("Average m1.medium price is %s over past 24 hour duration"%price)
        assert isinstance(price,float)
        pass

class TestUSW2CurrentSpotPrice(unittest.TestCase):

    def setUp(self):
        spc.URL="http://django-dev.heprc.uvic.ca:8080/ec2_spot_price_monitor/spot_price/"
        pass

    def tearDown(self):
        pass

    def testCurrSpotPrice(self):
        price=spc.get_current_us_west_2_spot_price("m1.medium")
        print ("Current price of m1.medium is %s"%price)
        assert isinstance(price,float)
        pass
    
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
        assert isinstance(result[0]['price'],float)
        #assert len(result)==10 or len(result)==9 or len(result)==11
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()