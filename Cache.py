from ResourceRecord import ResourceRecord
import time


class Cache:
    # ResourceRecord

    def __init__(self, record: ResourceRecord = None, cache_ttl=1000):
        # Initialize a DNS cache.
        self.data = {}
        self.cache_ttl = cache_ttl  # time to live
        self.cache_ttd = time.time() + self.cache_ttl  # time to die

    def refresh_cache(self):
        timestamp = time.time()
        if self.cache_ttd <= timestamp:  # time refresh
            black_list = []  # list delete
            for (i, rr) in self.data.items():
                if rr.ttl >= timestamp:  # ttl of resourcerecord
                    # can not delete dict when use iteritems
                    black_list.append(i)
            for i in black_list:
                del self.data[i]  # delete
            timestamp = time.time()
            self.cache_ttd = timestamp + self.cache_ttl

    def get(self, key):         # key = (name: str,rr_type: int, rr_class:int)
        self.refresh_cache()
        rr = self.data.get(key)
        #rr = self.data[key]
        if rr is None:# or rr._ttl <= time.time():
            return None
        return rr

    def put(self, key, record):        # record = ResourceRecord: object
        self.refresh_cache()
        self.data[key] = record
