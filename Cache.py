from ResourceRecord import ResourceRecord
import time


class Cache:
    # ResourceRecord

    def __init__(self, record:ResourceRecord = None, cache_ttl=1000):
        # Initialize a DNS cache.
        self.data = {}
        self.cache_ttl = cache_ttl # time to live
        self.cache_ttd = time.time() + self.cache_ttl # time to die

    def reset_cache(self):
        current_time = time.time()
        if self.cache_ttd <= current_time: # time to delete
            black_list = [] # list rr delete
            for (i, rr) in self.data.items():
                if rr.ttl <= current_time: # ttl of resourcerecord
                    black_list.append(i) 
            for i in black_list:
                del self.data[i] # delete
            current_time = time.time() 
            self.cache_ttd = current_time + self.cache_ttl

    def get(self, ntc):
        #ntc = (name: str,rr_type: int, rr_class:int)
        self.reset_cache()
        rr = self.data[ntc]
        if rr is None:
            return None
        return rr

    def put(self, ntc, record):
        #ntc = (name: str,rr_type: int, rr_class:int)
        #record = ResourceRecord: object
        self.reset_cache()
        self.data[ntc] = record
