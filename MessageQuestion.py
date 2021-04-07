# MessageQuestion class definition
from ResourceRecord import ResourceRecord


class MessageQuestion:
    # Static variables
    QTYPE = dict(ResourceRecord.TYPE)
    QTYPE.update(
        {"AXFR": 252, "MAILB": 253, "MAILA": 254, "*": 255})

    QCLASS = dict(ResourceRecord.CLASS)
    QCLASS.update({"*": 255})

    def __init__(self, qname: str, qtype: int, qclass: int):
        """Initialize a question."""
        if self._validate_(qname, qtype, qclass):
            self._qname = qname
            self._qtype = qtype
            self._qclass = qclass

    def _validate_(self, qname: str, qtype: int, qclass: int) -> bool:
        """Validate the QNAME, QTYPE, QCLASS before setting values."""
        if qname == "":
            return False
        elif len(qname.split(".")) <= 1:
            return False
        elif qtype not in MessageQuestion.QTYPE.values():
            return False
        elif qclass not in MessageQuestion.QCLASS.values():
            return False
        else:
            return True
