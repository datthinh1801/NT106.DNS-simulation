from ResourceRecord import ResourceRecord
import time


class Cache:
    # ResourceRecord

    def __init__(self, record: ResourceRecord = None, time_refresh=300):
        # Initialize a DNS cache.
        self._data = {}
        self._time_refresh = time_refresh  # time between 2 refresh
        self._time_refresh_next = time.time() + self._time_refresh  # time next refresh

    def refresh_cache(self):
        timestamp = time.time()
        # if "current time" is greater or equal than "time next refresh" mean can be refresh
        if self._time_refresh_next <= timestamp:
            black_list = []  # list "key" need delete
            for (i, rr) in self._data.items():
                # if time to die of RR > timestamp mean RR is out of date
                if rr._ttd >= timestamp:
                    black_list.append(i)
            """
            cannot delete dictionary when use iteritems
            =>>> use 2 step to delete
            """
            for i in black_list:
                del self._data[i]
            timestamp = time.time()
            self._time_refresh_next = timestamp + self._time_refresh

    def get(self, key):
        # key:(name: str,rr_type: int, rr_class:int)
        self.refresh_cache()
        rr = self._data.get(key)
        # rr = self.data[key] not return if data[key] None
        return rr

    def put(self, key, record):
        # key:(name: str,rr_type: int, rr_class:int)
        # record:ResourceRecord: object
        self.refresh_cache()
        self._data[key] = record
