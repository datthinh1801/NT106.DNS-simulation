from ResourceRecord import ResourceRecord
import time
import copy


class Cache_new:
    def __init__(self):
        self._data = None
        self._ttd = None

    def setter(self, record: ResourceRecord = None):
        self._data = copy.deepcopy(record)
        self._ttd = self._data._ttl + int(time.time())

    def getter(self):
        rr = copy.deepcopy(self._data)
        return rr


class CacheSystem:
    def __init__(self, refresh_time=300):
        self._data = {}
        self._refresh_time = refresh_time
        self._refresh_time_next = int(time.time()) + self._refresh_time

    def refresh(self):
        timestamp = int(time.time())
        if self._refresh_time_next <= timestamp:
            """
            neu set `_refresh_time_next` = 05:00:00 thi thoi gian hien tai phai la 05:00:00 hoac lon hon thi moi duoc phep refresh
            neu thoi diem hien tai chi la 04:59:59 hoac nho hon thi k duoc refresh
            """
            black_list = []
            for (i, cache) in self._data.items():
                if cache._ttd >= timestamp:
                    black_list.append(i)
            for i in black_list:
                del self._data[i]
            timestamp = time.time()
            self._refresh_time_next = timestamp + self._refresh_time

    def get(self, key):
        # key:(name: str,rr_type: int, rr_class:int)
        self.refresh()

        recordcache = self._data.get(key)
        if not recordcache is None:
            rr = recordcache.getter()
            return rr
        return None

    def put(self, key, data: ResourceRecord = None):
        # key:(name: str,rr_type: int, rr_class:int)
        # record:ResourceRecord: object
        self.refresh()

        recordcache = Cache_new()
        # print(type(recordcache),"put")
        recordcache.setter(data)

        self._data[key] = recordcache

"""
# ------testttt-----
RR1 = ResourceRecord("aaa.com", 1, 1, 1000, "1.2.3.4")
RR2 = ResourceRecord("bbb.com", 1, 1, 1000, "4.1.3")
RR3 = ResourceRecord("ccc.com", 1, 1, 1000, "3.1.2")
RR4 = ResourceRecord("ccc.", 1, 1, 1000, "3.1.2")


a = CacheSystem()

a.put(("bbb.com", 1, 1), RR2)
a.put(("ccc.com", 1, 1), RR3)
a.put(("ccc.", 1, 1), RR4)


print(a.get(("aaja.com", 1, 1)))

print(a.get(("bbb.com", 1, 1)).to_string())

print(a.get(("ccc.", 1, 1)).to_string())

"""
