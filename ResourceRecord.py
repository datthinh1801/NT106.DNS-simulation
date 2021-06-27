class ResourceRecord:
    # Static variables
    TYPE = {"A": 1, "NS": 2, "CNAME": 5, "SOA": 6, "WKS": 11,
            "PTR": 12, "HINFO": 13, "MX": 15, "TXT": 16}
    CLASS = {"IN": 1, "CH": 3, "HS": 4}

    INV_RRTYPE = {1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 11: "WKS",
                  12: "PTR", 13: "HINFO", 15: "MX", 16: "TXT"}

    INV_RRCLASS = {1: "IN", 3: "CH", 4: "HS"}

    def __init__(self, name: str, rr_type: int, rr_class: int, ttl: int, rdata: str):
        """
        Initialze a Resource Record.

        Parameters:
        name        -> hostname (at max 255 bytes)
        type        -> 2 bytes of the RR TYPE code
        rr_class    -> 2 bytes of the RR CLASS code
        ttl         -> a 32 bit signed integer specifies the cache interval of this RR (in seconds). 0 means do not cache
        rdata       -> data of corresponding query type

        [Alert] If some given parameters are invalid, the constructor will raise an Argument Exception.

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
        |___________|___________|

        class:
        ._______________________.
        |   Class   |   Int     |
        |___________|___________|
        |   IN      |   1       |
        |   CH      |   3       |
        |   HS      |   4       |
        |___________|___________|

        rdata:
        ._______________________________________.
        |    TYPE    |    VALUE                 |
        |____________|__________________________|
        | A          | A 32 bit Internet address|
        |____________|__________________________|
        | NS         | A <domain-name> of the   |
        |            | authoritative name server|
        |            | of the given hostname.   |
        |____________|__________________________|
        | CNAME      | A <domain-name> of       |
        |            | the given hostname.      |
        |____________|__________________________|
        | HINFO      | CPU:                     |
        |            | A string of CPU type.    |
        |            | OS:                      |
        |            | A string of OS type.     |
        |____________|__________________________|
        | MX         | PREFERENCE:              |
        |            | A 16 bit int of the      |
        |            | preference value         |
        |            | (lower - more prefered). |
        |            | EXCHAGNE:                |
        |            | A <domain-name> to       |
        |            | receive the mail.        |
        |____________|__________________________|

        """

        if self._validate_(name, rr_type, rr_class, ttl, rdata):
            name = name.lower()
            rdata = rdata.lower()
            self._name = name
            self._type = rr_type
            self._class = rr_class
            self._ttl = ttl
            self._rdata = rdata
            self._rdlength = len(self._rdata)
        else:
            self._name = None
            self._type = None
            self._class = None
            self._ttl = None
            self._rdlength = None
            self._rdata = None
            raise Exception(
                "Argument Exception while constructing a ResourceRecord object.")

    @staticmethod
    def _check_data_type_(*args, dtype: str) -> bool:
        """Check if variables are of dtype."""
        for arg in args:
            if str(type(arg)) != f"<class '{dtype}'>":
                return False
        return True

    def _validate_(self, name: str, rr_type: int, rr_class: int, ttl: int, rdata: str) -> bool:
        """Validate inputs before setting these values for the RR."""
        # check data types
        if not self._check_data_type_(name, rdata, dtype='str'):
            return False
        elif not self._check_data_type_(rr_type, rr_class, ttl, dtype='int'):
            return False

        # check if hostname is empty or exceeds the size limit of 255 bytes
        if name == "" or len(name) > 255:
            return False
        # check if hostname is not of the format label.label[.label[.label...]]
        elif len(name.split(".")) <= 1:
            return False
        # if hostname is of valid format, check if any label of hostname exceeds size limit of 63 bytes
        elif len(name.split(".")) > 1:
            for label in name.split("."):
                if len(label) > 63:
                    return False
        # check if rr_type is of invalid code
        elif rr_type not in ResourceRecord.TYPE.values():
            return False
        # check if rr_class is of invalid code
        elif rr_class not in ResourceRecord.CLASS.values():
            return False
        # check if ttl < 0
        elif ttl < 0:
            return False

        # overall true
        return True

    def to_string(self) -> str:
        """
        Convert to a string.
        The resulting has 1 line.
        #1 <hostname>;<type>;<class>;<ttl>;<value>
        """
        return self._name + ";" + str(self._type) + ";" + str(self._class) + ";" + str(self._ttl) + ";" + self._rdata

    def get_name(self):
        """Return the name of the record."""
        return self._name

    def get_type(self):
        """Return the type of the record"""
        return self._type

    def get_class(self):
        """Return the class of the record."""
        return self._class

    def get_ttl(self):
        """Return the ttl of the record."""
        return self._ttl

    def get_data(self):
        """Return the value of the record."""
        return self._rdata

    name = property(get_name)
    rr_type = property(get_type)
    rr_class = property(get_class)
    ttl = property(get_ttl)
    rdata = property(get_data)

    def __eq__(self, other):
        """Compare whether this ResourceRecord is equal to the other ResourceRecord."""
        return self.name == other.name and self.rr_type == other.rr_type and \
                self.rr_class == other.rr_class
