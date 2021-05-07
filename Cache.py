from ResourceRecord import ResourceRecord
from copy import deepcopy
from time import time


class Cache:
    def __init__(self, record: ResourceRecord):
        """
        Initialize a cache of a given record.
        ttd of the cache will be computed according to the ttl of the record.
        """
        self._record = record
        self._ttd = int(time()) + record.ttl

    def get_ttd(self):
        """Return the ttd of this cache."""
        return self._ttd

    def set_ttd(self, ttd: int):
        """Set the ttd of this cache to the given value."""
        if ttd > 0:
            self._ttd = ttd

    def get_rr(self):
        """Return a copy of the ResourceRecord of this cache."""
        return deepcopy(self._record)

    def __eq__(self, other):
        """
        Comparison between 2 cached records.
        If the name, type, and class of both are equal, they are equal;
        otherwise not equal.
        """
        if self.record == other.record:
            return True
        return False
    
    def to_string(self):
        """
        Convert the Cache object to a raw string cache for transmission.
        The resulting string has 1 lines.
        #1 record` + '/' + `ttd`
        """
        cache = ""
        cache += self._record.to_string() + "/" + str(self._ttd)
        return cache
        
    ttd = property(get_ttd, set_ttd)
    record = property(get_rr)
