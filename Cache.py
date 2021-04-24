from ResourceRecord import ResourceRecord
import time


class Cache:
    # ResourceRecord

    def __init__(self, record:ResourceRecord = None, cache_ttl=1000):
        # Initialize a DNS cache.
        self.data = {}
        self.cache_ttl = ttl # time to live
        self.cache_ttd = time.time() + self._cache_ttl # time to die

    def reset_cache(self):
        current_time = time.time()
        if self.cache_ttd >= current_time: # đã đến lúc để dọn dẹp 
            black_list = [] # hết hạn thì vô đây
            for (i, rr) in self.data.items():
                if rr.ttl >= current_time: # ttl of resourcerecord
                    black_list.append(k) # không thể xoá dictionary khi dùng iteritems
            for i in black_list:
                del self.data[i] # nên giờ mới xoá nè
            current_time = time.time() 
            self.cache_ttd = current_time + self.cache_ttl

    def get(self, key):
        #key = (name: str,rr_type: int, rr_class:int)
        self.reset_cache()
        v = self.data[key]
        if v is None or v.ttl <= time.time():
            return None
        return v

    def put(self, key, value):
        #key = (name: str,rr_type: int, rr_class:int)
        #value = ResourceRecord: object
            self.reset_cache()
            self.data[key] = value
