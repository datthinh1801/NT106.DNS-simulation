# MessageQuestion class definition
from ResourceRecord import ResourceRecord


class MessageQuestion:
    # Static variables
    # These string keys will be covnerted to integers in transmission
    QTYPE = dict(ResourceRecord.TYPE)
    QTYPE.update(
        {"AXFR": 252, "MAILB": 253, "MAILA": 254, "*": 255})

    QCLASS = dict(ResourceRecord.CLASS)
    QCLASS.update({"*": 255})
    
    INV_QTYPE = dict(ResourceRecord.INV_RRTYPE)
    INV_QTYPE.update(
        {252: "AXFR", 253: "MAILB", 254: "MAILA", 255: "*"})
    
    INV_QCLASS = dict(ResourceRecord.INV_RRCLASS)
    INV_QCLASS.update({255: "*"})


    def __init__(self, qname: str, qtype: int, qclass: int):
        """
        Initialize a question.

        Parameters:
        qname       -> Query hostname
        qtype       -> Query type
        qclass      -> Query class

        type:
        ._______________________.
        |   Type    |   Int     |
        |___________|___________|
        |   A       |   1       |
        |   NS      |   2       |
        |   CNAME   |   5       |
        |   SOA     |   6       |
        |   WKS     |   11      |
        |   PTR     |   12      |
        |   HINFO   |   13      |
        |   MX      |   15      |
        |   TXT     |   16      |
        |   AXFR    |   252     |
        |   MAILB   |   253     |
        |   MAILA   |   254     |
        |   *       |   255     |
        |___________|___________|
        class:
        ._______________________.
        |   Class   |   Int     |
        |___________|___________|
        |   IN      |   1       |
        |   CH      |   3       |
        |   HS      |   4       |
        |   *       |   255     |
        |___________|___________|

        """
        qname = qname.lower()

        if self._validate_(qname, qtype, qclass):
            self._qname = qname
            self._qtype = qtype
            self._qclass = qclass
        else:
            self._qname = None
            self._qtype = None
            self._qclass = None

    def _check_data_type_(self, *args, dtype: str) -> bool:
        """Check if variables are of dtype."""
        for arg in args:
            if str(type(arg)) != f"<class '{dtype}'>":
                return False
        return True

    def _validate_(self, qname: str, qtype: int, qclass: int) -> bool:
        """Validate the QNAME, QTYPE, QCLASS before setting values."""
        # check data types
        if not self._check_data_type_(qname, dtype='str'):
            return False
        elif not self._check_data_type_(qtype, qclass, dtype='int'):
            return False

        # check if hostname is empty or exceeds the size limit of 255 bytes
        if qname == "" or len(qname) > 255:
            return False
        # check if hostname is not of the format label.label[.label[.label...]]
        elif len(qname.split(".")) <= 1:
            return False
        # if hostname is of valid format, check if any label of the hostname exceeds the size limit of 63 bytes
        elif len(qname.split(".")) > 1:
            for label in qname.split("."):
                if len(label) > 63:
                    return False
        # check if qtype is of invalid code
        elif qtype not in MessageQuestion.QTYPE.values():
            return False
        # check if qclass is of invalid code
        elif qclass not in MessageQuestion.QCLASS.values():
            return False

        # overall true
        return True

    def is_None(self) -> bool:
        """Return True if this is a None-type MessageQuestion."""
        return self._qname == None

    def to_string(self) -> str:
        """
        Convert to a string.
        The resulting string has 1 line.
        #1 <hostname>;<qtype>;<qclass>
        """
        return self._qname + ";" + str(self._qtype) + ";" + str(self._qclass)
