from ResourceRecord import ResourceRecord


class Cache:
    # ResourceRecord
    """ Cache version 1
    """

    def __init__(self, record:ResourceRecord = None, ttl=1000):
        # Initialize a DNS cache.
        self.data = {}
        self.ttl = ttl # time to live
        self.ttd = time.time() + self.ttl # time to die

    def reset_cache(self):
        # Clean the cache if it's time to do so.
        now = time.time()
        if self.ttd <= now:
            keys_to_delete = []
            for (k, v) in self.data.iteritems():
                if v.expiration <= now:
                    keys_to_delete.append(k)
            for k in keys_to_delete:
                del self.data[k]
            now = time.time()
            self.ttd = now + self.ttl

    def get(self, key):
        #key = (name: str,rr_type: int, rr_class:int)
        self.reset_cache()
        v = self.data.get(key)
        if v is None or v.expiration <= time.time():
            return None
        return v

    def put(self, key, value):
        #key = (name: str,rr_type: int, rr_class:int)
        #value = ResourceRecord: object
            self.reset_cache()
            self.data[key] = value
