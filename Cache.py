try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

import time
import socket


class Cache(object):
    """ Cache version 1

    - data: A dictionary of cached data
    - cleaning_interval: The number of seconds between cleanings.  The default is 300 (5 minutes).
    - next_cleaning: The time the cache should next be cleaned (in seconds since the epoch.)

    """

    def __init__(self, cleaning_interval=300.0):
        # Initialize a DNS cache.
        

        self.data = {}
        self.cleaning_interval = cleaning_interval
        self.next_cleaning = time.time() + self.cleaning_interval
        self.lock = _threading.Lock()

    def _maybe_clean(self):
        # Clean the cache if it's time to do so.

        now = time.time()
        if self.next_cleaning <= now:
            keys_to_delete = []
            for (k, v) in self.data.iteritems():
                if v.expiration <= now:
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                del self.data[k]
            now = time.time()
            self.next_cleaning = now + self.cleaning_interval

    def get(self, key):
        #key = (qname: str, qtype: int, qclass:int)

        try:
            self.lock.acquire()
            self._maybe_clean()
            v = self.data.get(key)
            if v is None or v.expiration <= time.time():
                return None
            return v
        finally:
            self.lock.release()

    def put(self, key, value):

        #key = (qname: str, qtype: int, qclass:int)
        #value = answer object 
        """Associate key and value in the cache.
        @param key: the key
        @type key: (dns.name.Name, int, int) tuple whose values are the
        query name, rdtype, and rdclass.
        @param value: The answer being cached
        @type value: dns.resolver.Answer object
        """

        try:
            self.lock.acquire()
            self._maybe_clean()
            self.data[key] = value
        finally:
            self.lock.release()

    def flush(self, key=None):
        """Flush the cache.

        If I{key} is specified, only that item is flushed.  Otherwise
        the entire cache is flushed.

        @param key: the key to flush
        @type key: (dns.name.Name, int, int) tuple or None
        """

        try:
            self.lock.acquire()
            if not key is None:
                if self.data.has_key(key):
                    del self.data[key]
            else:
                self.data = {}
                self.next_cleaning = time.time() + self.cleaning_interval
        finally:
            self.lock.release()