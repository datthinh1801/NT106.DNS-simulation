# Message class definition
from MessageHeader import *
from MessageQuestion import *

#########################################
#                 NOTE                  #
#########################################
# DNS is case-insensitive
# various objects & parameters in DNS have size limits (refer to RFC 1035 for details)


class Message:
    def __init__(self):
        """Initialize a Message."""
        # header of the message
        self._header = MessageHeader()
        # fields describe a question to a name server
        self._question = MessageQuestion()
        # a possibly empty list of RRs
        self._answer = []
        # RRs point to the authoritative name server (which answers the question)
        self._authority = []
        # Additional information relates to the query but not strictly answer the question
        self._additional = []
