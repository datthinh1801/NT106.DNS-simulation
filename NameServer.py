from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ResourceRecord import ResourceRecord
import dns.query
import dns.zone
import dns.resolver
import threading

import socket
from ParseString import parse_string_msg

QTYPE = dict(ResourceRecord.TYPE)
QTYPE.update(
    {"AXFR": 252, "MAILB": 253, "MAILA": 254, "*": 255})

QCLASS = dict(ResourceRecord.CLASS)
QCLASS.update({"*": 255})


def Get_key_from_values(dicts: dict = None, key=None):
    key_list = list(dicts.keys())
    value_list = list(dicts.values())
    return key_list[value_list.index(key)]


# Nameserver class definition
class NameServer:
    def __init__(self, Cache: bool = False):
        """
        Receive the query from resolver in raw text format and Parse raw text to Messages Object 
        to handle the query then send respone or continously send query to other zonr( recursive-query)
        """
        self.__zone = None
        self.__cache = Cache

    def Query_handle(self, query_message: Message = None) -> Message:
        # query qr == 0 ? qr == 1
        if query_message._header._qr == 1:
            header = query_message._header
            question = query_message._question
            if header._rd == True:
                message_answer = self.Recursive_query(query_message)
                return message_answer
                # hanle wrong answer ... !!!! (  not implement yet )
            else:
                answer = self.Non_Recursive_query(header, question)

    def Convert_response_answer_to_response_message(self, response_anwser: dns.message = None,
                                                    message_query: Message = None) -> Message:

        message_response = Message(request=message_query)
        # express message is response
        message_response._header._qr = 1

        # add eache section to message_response 1 : answer section. 2: authority section, 3: additional section
        for i in range(1, 4):
            for RRs in response_anwser.sections[i]:
                name = RRs.name
                rr_type = RRs.rdtype
                rr_class = RRs.rdclass
                ttl = RRs.ttl
                rdata = RRs[0]
                resource_records = ResourceRecord(str(name), int(
                    rr_type), int(rr_class), int(ttl), str(rdata))
                if i == 1:
                    message_response.add_a_new_record_to_answer_section(
                        resource_records)
                if i == 2:
                    for j in range(len(RRs)):
                        rdata = RRs[j]
                        message_response.add_a_new_record_to_authority_section(ResourceRecord(
                            str(name), int(rr_type), int(rr_class), int(ttl), str(rdata)))
                if i == 3:
                    message_response.add_a_new_record_to_additional_section(
                        resource_records)

        # return message response
        return message_response

    def Recursive_query(self, message_query: Message = None) -> Message:
        result = self.Search_Record_In_Cache(message_query)
        if result == None:
            result = self.Search_Record_In_ZoneFile(message_query)
            if result == None:
                result = self.Query_Out(message_query)

        return result

    def Non_Recursive_query(self, header: MessageHeader = None, question: MessageQuestion = None):
        print()

    def Search_Record_In_Cache(self, qname: str = None, qtype: str = None):
        return None

    def Search_Record_In_ZoneFile(self, qname: str = None, qtype: str = None):
        return None

    def Query_Out(self, message_query: Message = None):
        qname = message_query._question._qname
        qtype = message_query._question._qtype
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8']
        resolve_query = resolver.resolve(qname, Get_key_from_values(
            QTYPE, qtype), raise_on_no_answer=False)
        print("\n-----")
        print("request: ", message_query._question.to_string())
        print("response: ", resolve_query.response)
        print("-----\n")
        # handle error query here
        response_message = self.Convert_response_answer_to_response_message(
            resolve_query.response, message_query)

        return response_message

    def start_listening_TCP(self):
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 9999)
        buffersize = 10000

        # Bind the socket to the port
        sock.bind(server_address)

        # listen for incomming connections
        print("TCP waiting...")
        sock.listen(0)

        while True:
            # wait for a connection
            connection, client_address = sock.accept()
            try:
                byteData = connection.recv(buffersize)
                data_receive = byteData.decode('utf-8')
                if data_receive:
                    message_query = parse_string_msg(data_receive)
                    message_result = self.Query_handle(message_query)
                    # send back the result to resolver here

                    response = str.encode(message_result.to_string())
                    connection.sendall(response)
                else:
                    break  # code more to print out error
            finally:
                connection.close()

    def start_listening_UDP(self):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 20000)
        buffersize = 2048

        # bind the socket to the port
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) -> this is for overlap port
        sock.bind(server_address)
        # sock.listen(1)
        print("UDP waiting...")
        while True:
            byteData = sock.recvfrom(buffersize)
            data_receive = byteData[0].decode('utf-8')
            client_address = byteData[1]
            if data_receive:
                message_query = parse_string_msg(data_receive)
                message_result = self.Query_handle(message_query)
                # send back the result to resolver here
                response = str.encode(message_result.to_string())

                sock.sendto(response, client_address)
        print("disconnect")


"""
.3.13. SOA RDATA format

    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    /                     MNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    /                     RNAME                     /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    SERIAL                     |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    REFRESH                    |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     RETRY                     |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    EXPIRE                     |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    MINIMUM                    |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

where:

MNAME           The <domain-name> of the name server that was the
                original or primary source of data for this zone.

RNAME           A <domain-name> which specifies the mailbox of the
                person responsible for this zone.

SERIAL          The unsigned 32 bit version number of the original copy
                of the zone.  Zone transfers preserve this value.  This
                value wraps and should be compared using sequence space
                arithmetic.

REFRESH         A 32 bit time interval before the zone should be
                refreshed.

RETRY           A 32 bit time interval that should elapse before a
                failed refresh should be retried.

EXPIRE          A 32 bit time value that specifies the upper limit on
                the time interval that can elapse before the zone is no
                longer authoritative.

"""

name_sv = NameServer()


thr_udp = threading.Thread(target=name_sv.start_listening_UDP, args=())
thr_udp.start()


thr_tcp = threading.Thread(target=name_sv.start_listening_TCP, args=())
thr_tcp.start()
