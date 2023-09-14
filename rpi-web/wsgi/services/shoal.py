from base import RpiService
import redis
import collections



class ShoalService(RpiService):
    """
    This class implements the Shoal Service.
    It will query the redis database to get information about
    the status of the service.
    """

    def __init__(self, d):
        RpiService.__init__(self, d)
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)


    def getUsage(self):
        # TODO
        # return int(self.r.get('shoal-usage'))
        return 0


    def getLastReset(self):
        # TODO
        #return self.r.get('shoal-reset-date')
        return '2015-01-01T00:00:00Z'

