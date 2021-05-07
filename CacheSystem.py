from ResourceRecord import ResourceRecord
from time import time
from copy import deepcopy
from Cache import Cache

class CacheSystem:
    def __init__(self, refresh_time=300):
        self._database = []
        self._refresh_time = refresh_time
        self._next_refresh_time = int(time()) + self._refresh_time

    def refresh(self):
        """Refresh cache database."""
        timestamp = int(time())
        if timestamp >= self._next_refresh_time:
            black_list = []
            for i in range(len(self._database)):
                if self._database[i].ttd >= timestamp:
                    black_list.append(i)

            for i in black_list:
                del self._database[i]

            # Reset the next time to refresh
            timestamp = int(time())
            self._next_refresh_time = timestamp + self._refresh_time

    def get(self, name: str, rr_type: int = 1, rr_class: int = 1) -> ResourceRecord:
        """
        Get the ResourceRecord that matches the given attributes.
        This method return the cache if matches; otherwise None.

        Parameter:
        key     => A tuple of (name: str, rr_type: int, rr_class: int)
        """
        self.refresh()

        queried_record = ResourceRecord(name=name, rr_type=rr_type, rr_class=rr_class, ttl=0, rdata="")
        for cache in self._database:
            if queried_record == cache.record and time() <= cache._ttd:
                return cache.record

        return None

    def put(self, record: ResourceRecord):
        """
        Cache a ResourceRecord in the Cache database.
        If an existing record is already cached, update its ttl and ttd.
        """
        self.refresh()

        cache = Cache(record)
        # Check if a cache of the given record is already cached in the database
        for i in range(len(self._database)):
            # If exists, update ttd
            if cache == self._database[i]:
                self._database[i].ttd = cache.ttd
                return

        # If not exists, append it to the database
        self._database.append(cache)

    def to_string(self):
        """
        Convert the CacheSystem object to a raw string cachesystem for transmission.
        The resulting string has multiple lines.
        #1      Refresh Time
        #2      Next Refresh Time      
        #Remaining lines are the numbers of cache
        """
        string = ""
        string += str(self._refresh_time) + "\n"
        string += str(self._next_refresh_time) + "\n"
        for i in self._database:
            string += i.to_string() + "\n"
        return string

"""
def parse_string_cache(cachestr:str) -> Cache:
    # Parse a cache string to a Cache object.
    fields = cachestr.split('/')
    rr = parse_string_resource_record(fields[0])
    ttd = int(fields[1])
    cache = Cache(rr)
    cache._ttd = ttd
    return cache

def parse_string_cachesystem(cachesys:str) -> CacheSystem:
    # Parse a CacheSystem string to a CacheSystem object.
    lines = cachesys.splitlines()
    Sys = CacheSystem()
    Sys._refresh_time = int(lines[0])
    Sys._next_refresh_time = int(lines[1])
    for i in range (2, len(lines)):
        cache = parse_string_cache(lines[i])
        Sys._database.append(cache)
    return Sys
"""