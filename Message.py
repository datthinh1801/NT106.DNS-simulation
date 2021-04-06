# Message class definition
from MessageHeader import *
from MessageQuestion import *

#########################################
#                 NOTE                  #
#########################################
# DNS is case-insensitive
# various objects & parameters in DNS have size limits (refer to RFC 1035 for details)


class Message:
    def __init__(self, str_data=None):
        self._header = MessageHeader()
        self._question = MessageQuestion()

    def getIP(self):
        return ""
