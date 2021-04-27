from ResourceRecord import ResourceRecord
import time

# key = ("aaa", 1, 1)


# , key = ("aaa", 1, 1)

class Cache:
    # ResourceRecord

    def __init__(self, record: ResourceRecord = None, cache_ttl=1000):
        # Initialize a DNS cache.
        self.data = {}
        self.cache_ttl = cache_ttl  # time to live
        self.cache_ttd = time.time() + self.cache_ttl  # time to die

    def reset_cache(self):
        timestamp = time.time()
        if self.cache_ttd <= timestamp:  # đã đến lúc để dọn dẹp
            black_list = []  # hết hạn thì vô đây
            for (i, rr) in self.data.items():
                if rr.ttl >= timestamp:  # ttl of resourcerecord
                    # không thể xoá dictionary khi dùng iteritems
                    black_list.append(i)
            for i in black_list:
                del self.data[i]  # nên giờ mới xoá nè
            timestamp = time.time()
            self.cache_ttd = timestamp + self.cache_ttl

    def get(self, key):
        # key = (name: str,rr_type: int, rr_class:int)
        self.reset_cache()
        rr = self.data[key]
        if rr is None:  # or rr.ttl <= time.time():
            return None
        return rr

    def put(self, key, record):
        # key = (name: str,rr_type: int, rr_class:int)
        # record = ResourceRecord: object
        self.reset_cache()
        self.data[key] = record


a = Cache()

RR1 = ResourceRecord("aaa", 1, 1, 1000, "123")
RR2 = ResourceRecord("bbb", 1, 1, 1000, "413")
RR3 = ResourceRecord("ccc", 1, 1, 1000, "312")


a.put(("aaa", 1, 1), RR1)
a.put(("bbb", 1, 1), RR2)
a.put(("ccc", 1, 1), RR3)

rr = a.get(("aaa", 1, 1))
if rr:
    print(rr.to_string())
else:
    print("None")
