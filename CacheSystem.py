from ResourceRecord import ResourceRecord
import time
import copy
from ParseString import parse_string_resource_record

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
    def to_string(self):
        return self._data.to_string() + "+" + str(self._ttd)

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
        if not recordcache is None or recordcache._ttd > time.time():
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

    def CacheSystem_to_string(self):
        cachesys = ""
        cachesys += str(self._refresh_time) + "\r\n"
        cachesys += str(self._refresh_time_next) + "\r\n"
        for (i, cache) in self._data.items():
            cachesys += str(i) + ":"
            cachesys += cache.to_string() + "\r\n"
        return cachesys

def Parse_string_key(key:str):
    key = key.replace('(', '')
    key = key.replace(')', '')
    fields = key.split(',')
    return (fields[0], int(fields[1]), int(fields[2]))

def Parse_string_cache(cache:str) -> Cache_new:
    fields = cache.split('+')
    rr = parse_string_resource_record(fields[0])
    ttd = int(fields[1])
    cachenew = Cache_new()
    cachenew._data = rr
    cachenew._ttd = ttd
    return cachenew

def Parse_string_cache_system(cachesys:str) -> CacheSystem:
    lines = cachesys.splitlines()
    # lines = cachesys.split('\r\n')
    cachesystem = CacheSystem()
    cachesystem._refresh_time = int(lines[0])
    cachesystem._refresh_time_next = int(lines[1])
    for line in range(2,len(lines)):
        fields = lines[line].split(':')
        key = Parse_string_key(fields[0])
        cache = Parse_string_cache(fields[1])
        cachesystem._data[key] = cache
    return cachesystem




# ------testttt-----
RR1 = ResourceRecord("aaa.com", 1, 1, 1000, "1.2.3.4")
RR2 = ResourceRecord("bbb.com", 1, 1, 1000, "4.1.3")
RR3 = ResourceRecord("ccc.com", 1, 1, 1000, "3.1.2")
RR4 = ResourceRecord("ccc.", 1, 1, 1000, "3.1.2")

a = CacheSystem()

a.put(("bbb.com", 1, 1), RR2)
a.put(("ccc.com", 1, 1), RR3)
a.put(("ccc.", 1, 1), RR4)

print("--check in cache a--")
print(a.get(("bbb.com", 1, 1)).to_string())

string = a.CacheSystem_to_string()
print(string)

b = Parse_string_cache_system(string)

print("--check in cache b--")
print(b.get(("bbb.com", 1, 1)).to_string())

"""
string= a.CacheSystem_to_string()
print(string)

print(a.get(("aaja.com", 1, 1)))

print(a.get(("bbb.com", 1, 1)).to_string())

print(a.get(("ccc.", 1, 1)).to_string())
"""