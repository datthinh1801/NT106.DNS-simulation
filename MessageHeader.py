# MessageHeader class definition
import random


class MessageHeader:
    def __init__(self, qr=0, opcode=0, aa=False, tc=False, rd=True, ra=True, rcode=0, qdcount=0, ancount=0, nscount=0, arcount=0):
        """
        Initialize the header of a Message.
        Default values:
        QR = 0 --> This Message is a query.
        OPCODE = 0 --> This Message is a standard query.
        AA = False --> This is a query, so it has nothing to do with Authoritative Answer flag.
        TC = False --> This Message is not truncated.
        RD = True --> Ask for recursive query.
        RA = True --> Resursion available by default.
        All other fields are initialized to 0.
        """
        # 16-bit identifier
        self._id = random.randint(0, pow(2, 16) - 1)
        # 1-bit flag specifies if this Message is a query (0) or a response (1)
        self._qr = qr
        # 4-bit flag (values range from 0 to 15) specifies the kind of query
        self._opcode = opcode
        # 1-bit Authoritative Answer - valid in responses, specifies whether an authoritative server answers the request
        # this only see the first RR to set the bit
        self._aa = aa
        # [TrunCation] 1-bit flag specifies if the Message is truncated
        self._tc = tc
        # [Recursion Desired] 1-bit flag specifies the name server to query recursively
        self._rd = rd
        # [Recursive Available] 1-bit flag specifies if the name server supports recursive query
        self._ra = ra
        # Reserved for future use, must be 0 in all Messasges
        self._z = 0
        # [Response code] 4-bit field specifies error
        self._rcode = rcode
        # 16-bit int specifies the number of questions
        self._qdcount = qdcount
        # 16-bit int specifies the number of RRs in the answer section
        self._ancount = ancount
        # 16-bit int specifies the number of name server RRs in the Authority section
        self._nscount = nscount
        # 16-bit int specifies the number of RRs in the Additional Records section
        self._arcount = arcount

    def set_qr_flag(self, flag: bool) -> None:
        """
        Set the query flag.
        0 -> A query
        1 -> A response
        """
        self._qr = flag

    def set_opcode(self, code: int) -> None:
        """
        Set the opcode.
        0 -> Standard query (QUERY)
        1 -> Inverse query  (IQUERY)
        2 -> Server status request (STATUS)
        3-15 -> Reseverd for future use
        """
        if code >= 0 and code <= 15:
            self._opcode = code

    def set_authoritative_flag(self) -> None:
        """[Only valid in responses] Set the authoritative flag to True."""
        self._aa = True

    def set_truncate_flag(self) -> None:
        """[Only valid in responses] Set the truncate flag to True"""
        self._tc = True

    def clear_recursion_desire(self) -> None:
        """Clear the recursion desire flag."""
        self._rd = False

    def clear_recursion_available(self) -> None:
        """Clear the recursion available flag."""
        self._ra = False

    def set_rcode(self, code: int) -> None:
        """
        Set the response code.
        0 -> No error
        1 -> Format error - The name server doesn't understand the query.
        2 -> Server failure - The name server had a problem while processing the query.
        3 -> Name error - [Available in Authoritative name servers only] The queried domain name does not exist.
        4 -> Not implemented - The name server does not support the requested kind of query.
        5 -> Refused - The name server refuses to perform the specified operation for policy reasons.
        6-15 -> Reserved for future use.
        """
        if code >= 0 and code <= 15:
            self._rcode = code

    def set_qdcount(self, field: str, count: int) -> None:
        """
        Set the field to a given count value.
        field = ["qd", "an", "ns", "ar"]
        """
        if count >= 0:
            if field == "qd":
                self._qdcount = count
            elif field == "an":
                self._ancount = count
            elif field == "ns":
                self._nscount = count
            elif field == "ar":
                self._arcount = count
