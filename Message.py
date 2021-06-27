# Message class definition
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ResourceRecord import ResourceRecord
from copy import copy


#########################################
#                 NOTE                  #
#########################################
# DNS is case-insensitive
# various objects & parameters in DNS have size limits (refer to RFC 1035 for details)


class Message:
    def __init__(self, request=None, header: MessageHeader = None, question: MessageQuestion = None):
        """
        Initialize a Message.

        Parameters:
        request         -> [Response Only] The request Message object that this Message will reply to.
                           This will copy the Question section and the Header section from the request to the response.
        header          -> [Request Only] The header section of the message.
        question        -> [Request Only] The question section of the message.

        Properties:
        _header         -> A MessageHeader object
        _question       -> A MessageQuession object
        _answer         -> A possibly empty list of RRs represents answers
        _authority      -> A possibly empty list of RRs represents name servers
        _additional     -> A possibly empty list of RRs
        """

        self._header = None
        self._question = None
        self._answer = []
        self._authority = []
        self._additional = []

        if request is not None:
            self._header = copy(request.header)
            self._question = copy(request.question)
            self.set_header_flags(qr=1)
        elif header is not None and question is not None:
            self._header = copy(header)
            self._question = copy(question)
        else:
            raise Exception("Parameter Error")

        self._set_header_flags_automatically()

    def _set_header_flags_automatically(self):
        """
        Set header flags based on properties of the Message object.
        This method will set the following flags:
        - QR
        - RCODE
        - QDCOUNT
        - ANCOUNT
        - NSCOUNT
        - ARCOUNT
        """
        # Check Question section and set related flags
        if self._question.is_none():
            self._header.set_rcode(1)  # Format error
        else:
            self._header.set_count("qd", 1)

        # check Count sections and set related flags
        if len(self._answer) > 0:
            self._header.set_count("an", len(self._answer))
        if len(self._authority) > 0:
            self._header.set_count("ns", len(self._authority))
        if len(self._additional) > 0:
            self._header.set_count("ar", len(self._additional))

    def to_string(self) -> str:
        """
        Convert the Message object to a raw string message for transmission.
        The resulting string has multiple lines.
        #1-6    Header's fields
        #7      Question
        #Remaining lines are the numbers of records of each section
        """
        msg = ""
        msg += self.header.to_string() + "\n"
        msg += self.question.to_string() + "\n"
        for record in self.answers:
            msg += record.to_string() + "\n"
        for record in self.authorities:
            msg += record.to_string() + "\n"
        for record in self.additional:
            msg += record.to_string() + "\n"
        return msg

    def add_a_new_record_to_answer_section(self, record: ResourceRecord):
        """Add a new record to the ANSWER section."""
        self._answer.append(record)
        self._set_header_flags_automatically()

    def add_a_new_record_to_authority_section(self, record: ResourceRecord):
        """Add a new record to the AUTHORITY section."""
        self._authority.append(record)
        self._set_header_flags_automatically()

    def add_a_new_record_to_additional_section(self, record: ResourceRecord):
        """Add a new record to the ADDITIONAL section."""
        self._additional.append(record)
        self._set_header_flags_automatically()

    def set_header_flags(self, qr: int = None, opcode: int = None, aa: bool = None, tc: bool = None, rd: bool = None,
                         ra: bool = None, rcode: int = None):
        """
        Set specified header's flags.
        flag=None means not affected.
        """
        self._set_header_flags_automatically()

        if qr is not None:
            self._header.set_qr_flag()
        if opcode is not None:
            self._header.set_opcode(opcode)
        if aa is not None and aa:
            self._header.set_authoritative_flag()
        if tc is not None and tc:
            self._header.set_truncate_flag()
        if rd is not None and not rd:
            self._header.clear_recursion_desire_flag()
        if ra is not None and not ra:
            self._header.clear_recursion_available_flag()
        if rcode is not None:
            self._header.set_rcode(rcode)

    def get_answer_records(self):
        """Return a copy of the list of ResourceRecords in the Answer section."""
        return copy(self._answer)

    def get_authority_records(self):
        """Return a copy of the list of ResourceRecords in the Authority section."""
        return copy(self._authority)

    def get_additional_records(self):
        """Return a copy of the list of ResourceRecords in the Additional section."""
        return copy(self._additional)

    def get_header(self):
        """Return a copy of the header of the message."""
        return copy(self._header)

    def get_question(self):
        """Return a copy of the question of the message."""
        return copy(self._question)

    """
    Using property feature to ease the protected property access.
    From now, we can use self.header to get a copy of the header instead of invoking the get_header() method.
    """
    header = property(get_header)
    question = property(get_question)
    answers = property(get_answer_records)
    authorities = property(get_authority_records)
    additional = property(get_additional_records)
