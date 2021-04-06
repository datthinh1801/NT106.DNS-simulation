# MessageHeader class definition

class MessageHeader:
    def __init__(self):
        self._id = ""            # identifier
        self._qr = ""            # 0 for query; 1 for response
        self._opcode = ""        # kind of query
        self._aa = ""            # [valid in response] 1 if the response was returned from an authoritative server
        self._tc = ""            # 1 if the message is truncated
        self._rd = ""            # 1 if desire for recursion
        self._ra = ""            # [valid in response] 1 if the response was returned from a recursion-available server
        self._z = ""             # must be 0
        self._rcode = ""         # [valid in response] specify error code
        self._qdcount = ""       # the number of entries in the question section
        self._ancount = ""       # the number of RRs in the answer section
        self._nscount = ""       # the number of name server RRs
        self._arcount = ""       # the number of RRs in the additional records section
