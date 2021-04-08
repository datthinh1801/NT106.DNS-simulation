# Message class definition
from MessageHeader import *
from MessageQuestion import *

#########################################
#                 NOTE                  #
#########################################
# DNS is case-insensitive
# various objects & parameters in DNS have size limits (refer to RFC 1035 for details)


class Message:
    def __init__(self, request: Message = None, header: MessageHeader = None, question: MessageQuestion = None):
        """
        Initialize a Message.

        Parameters:
        request         -> [Response Only] The request that this Message will reply to.
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

        if request != None:
            self._header = request._header
            self._question = request._question
        elif header != None and question != None:
            self._header = header
            self._question = question
        else:
            raise Exception("Parameter Error")

    def set_header_flags_automatically(self):
        """
        Set header flags based on properties of the Message object.
        This helper method will set the following flags:
        - QR
        - RCODE
        - QDCOUNT
        - ANCOUNT
        - NSCOUNT
        - ARCOUNT
        """
        # Check Question section and set related flags
        if self._question.is_None():
            self._header.set_rcode(1)   # Format error
        else:
            self._header.set_count("qd", 1)

        # check Count sections and set related flags
        if len(self._answer) > 0:
            self._header.set_count("an", len(self._answer))
            # If there is some answers, this is a response Message
            self._header.set_qr_flag(1)
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
        #Remaining lines are records (inspect the header for their quantities)
        """
        msg = ""
        msg += self._header.to_string() + "\n"
        msg += self._question.to_string() + "\n"
        for record in self._answer:
            msg += record.to_string() + "\n"
        for record in self._authority:
            msg += record.to_string() + "\n"
        for record in self._additional:
            msg += record.to_string() + "\n"
        return msg

    def add_new_records_to_answer_section(self, records: list):
        """Add new records to the ANSWER section."""
        self._answer += records

    def add_records_to_authority_section(self, records: list):
        """Add new records to the AUTHORITY section."""
        self._authority += records

    def add_records_to_additional_section(self, records: list):
        """Add new records to the ADDITIONAL section."""
        self._additional += records
