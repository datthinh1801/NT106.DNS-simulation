# MessageHeader class definition
import random


class MessageHeader:
    def __init__(self, id: int = None, qr: int = 0, opcode: int = 0, aa: bool = False, tc: bool = False, rd: bool = True, ra: bool = True, rcode: int = 0, qdcount: int = 0, ancount: int = 0, nscount: int = 0, arcount: int = 0):
        """
        Initialize the header of a Message.

        Default values:
        QR = 0      --> This Message is a query.
        OPCODE = 0  --> This Message is a standard query.
        AA = False  --> This is a query, so it has nothing to do with Authoritative Answer flag.
        TC = False  --> This Message is not truncated.
        RD = True   --> Ask for recursive query.
        RA = True   --> Resursion available by default.
        RCODE = 0   --> No error

        All other fields are initialized to 0.
        """
        # 16-bit identifier
        self._id = random.randint(0, pow(2, 16) - 1) if id == None else id
        # 1-bit flag specifies if this Message is a query (0) or a response (1)
        self._qr = qr
        # 4-bit flag (values range from 0 to 15) specifies the kind of query
        self._opcode = opcode
        # 1-bit Authoritative Answer - valid in responses, specifies whether an authoritative server answers the request
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

    def set_qr_flag(self) -> None:
        """[Only valid in responses] Set the query flag."""
        self._qr = 1

    def set_opcode(self, code: int) -> None:
        """
        Set the opcode.
        0 -> Standard query (QUERY)
        1 -> Inverse query  (IQUERY)
        2 -> Server status request (STATUS)
        3-15 -> Reseverd for future use
        """
        if code in [0, 15]:
            self._opcode = code

    def set_authoritative_flag(self) -> None:
        """[Only valid in responses] Set the authoritative flag to True."""
        self._aa = True

    def set_truncate_flag(self) -> None:
        """[Only valid in responses] Set the truncate flag to True."""
        self._tc = True

    def clear_recursion_desire_flag(self) -> None:
        """Clear the recursion desire flag."""
        self._rd = False

    def clear_recursion_available_flag(self) -> None:
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
        if code in [0, 15]:
            self._rcode = code

    def set_count(self, field: str, count: int) -> None:
        """
        Set the field to a given count value.
        field = ("qd", "an", "ns", "ar")
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

    def to_string(self) -> str:
        """
        Convert to a string.
        The resulting string has 6 lines:

        #1 ID in hex
        #2 16-bit flags
        #3 QDCOUNT
        #4 ANCOUNT
        #5 NSCOUNT
        #6 ARCOUNT
        """
        string = ""
        # get ID
        string += str(self._id) + "\n"

        # get flags
        header = ""
        # QR flag 1-bit
        header += str(int(self._qr))
        # OPCODE 4-bit
        header += bin(self._opcode)[2:].rjust(4, "0")
        # AA flag 1-bit
        header += str(int(self._aa))
        # TC flag 1-bit
        header += str(int(self._tc))
        # RD flag 1-bit
        header += str(int(self._rd))
        # RA flag 1-bit
        header += str(int(self._ra))
        # Z flag 3-bit
        header += bin(self._z)[2:].rjust(3, "0")
        # RCODE 4-bit
        header += bin(self._rcode)[2:].rjust(4, "0")

        string += hex(int(header, 2)) + "\n"

        # get counts
        string += str(self._qdcount) + "\n"
        string += str(self._ancount) + "\n"
        string += str(self._nscount) + "\n"
        string += str(self._arcount)
        return string
