from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ResourceRecord import ResourceRecord
import dns.query
import dns.zone
import dns.resolver
import dns.exception
import threading
from CacheSystem import CacheSystem

import socket
from ParseString import parse_string_msg
from configurator import Configurator


# Nameserver class definition
class NameServer:
    def __init__(self):
        """
        Receive the query from resolver in raw text format and Parse raw text to Messages Object
        to handle the query then send response or continuously send query to other zone(recursive-query)
        """
        self.ZONE = None
        self.CACHE = CacheSystem()
        Configurator.config_server(5353, 5252)

    def handle_query(self, query_message: Message) -> Message:
        # query qr == 0 (a query) ? qr == 1 (a response)
        if query_message.header.qr == 0:
            header = query_message.header
            question = query_message.question
            if header.rd is True:
                message_answer = self.recursive_query(query_message)
                return message_answer
            else:
                answer = self.non_recursive_query(header, question)
                return answer

    @staticmethod
    def convert_response_answer_to_response_message(response_answer: dns.message = None,
                                                    message_query: Message = None) -> Message:
        message_response = Message(request=message_query)
        # set the qr flag to 1, which indicates a response
        message_response.header.set_qr_flag()

        # add each section to message_response
        # 1 : answer section
        # 2: authority section
        # 3: additional section
        for i in range(1, 4):
            for RRs in response_answer.sections[i]:
                name = RRs.name
                rr_type = RRs.rdtype
                rr_class = RRs.rdclass
                ttl = RRs.ttl
                rdata = RRs[0]
                resource_records = ResourceRecord(str(name), int(
                    rr_type), int(rr_class), int(ttl), str(rdata))
                if i == 1:
                    message_response.add_a_new_record_to_answer_section(resource_records)
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

    def recursive_query(self, message_query: Message) -> Message:
        result = self.search_record_in_cache(message_query.question.qname, message_query.question.qtype,
                                             message_query.question.qclass)
        if result is None:
            result = self.search_record_in_zonefile(message_query.question.qname, message_query.question.qtype)

        if result is None:
            result = self.query_out(message_query)

        return result

    def non_recursive_query(self, header: MessageHeader, question: MessageQuestion) -> Message:
        return None

    def search_record_in_cache(self, qname: str, qtype: int = 1, qclass: int = 1):
        return self.CACHE.get(qname, qtype, qclass)

    def search_record_in_zonefile(self, qname: str = None, qtype: str = None) -> ResourceRecord:
        return None

    def query_out(self, message_query: Message):
        qname = message_query.question.qname
        qtype = message_query.question.qtype
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8']
        try:
            resolve_query = resolver.resolve(qname, message_query.question.INV_QTYPE[qtype], raise_on_no_answer=False)
        except dns.exception.DNSException as e:
            response_message = "Failed-" + str(e)
            return response_message

        # print("\n-----")
        # print("request: ", message_query.question.to_string())
        # print("response: ", resolve_query.response)
        # print("-----\n")

        # handle error query here
        response_message = self.convert_response_answer_to_response_message(resolve_query.response, message_query)

        self.save_to_cache_system(response_message)
        return response_message

    def save_to_cache_system(self, response: Message):
        """Save all RRs in the response to the cache system."""
        for answer in response.answers:
            self.CACHE.put(answer)

        for authority in response.authorities:
            self.CACHE.put(authority)

        for add in response.additional:
            self.CACHE.put(add)

    def start_listening_tcp(self):
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (Configurator.SERVER_IP, Configurator.SERVER_TCP_PORT)

        # Bind the socket to the port
        sock.bind(server_address)

        # listen for incoming connections
        print(f"[SERVER]\t Listening for TCP connections at {Configurator.SERVER_IP}:" +
              f"{Configurator.SERVER_TCP_PORT}...")
        sock.listen(0)

        while True:
            # wait for a connection
            connection, client_address = sock.accept()
            try:
                byte_data = connection.recv(Configurator.BUFFER_SIZE)
                data_receive = byte_data.decode('utf-8')
                if data_receive:
                    message_query = parse_string_msg(data_receive)

                    # print("\n-----")
                    # print("request: ", data_receive)

                    # message question
                    msg_question = message_query.question

                    # find in cache first
                    cached_record = self.CACHE.get(msg_question.qname, msg_question.qtype, msg_question.qclass)
                    if cached_record is not None:
                        # print("in cache")
                        message_result = Message(request=message_query)
                        message_result.add_a_new_record_to_answer_section(cached_record)
                    else:
                        message_result = self.handle_query(message_query)
                    # send the result back to resolver here

                    if not isinstance(message_result, str):
                        message_result = message_result.to_string()

                    # print("response: ", message_result)
                    # print("-----\n")

                    response = message_result.encode('utf-8')
                    connection.sendall(response)
                else:
                    break  # more code needed to print out error
            except Exception as e:
                print("Exception occurs while handle a tcp connection. " + str(e))
            finally:
                connection.close()

    def start_listening_udp(self):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (Configurator.SERVER_IP, Configurator.SERVER_UDP_PORT)

        # bind the socket to the port
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) -> this is for overlap port
        sock.bind(server_address)
        print(f"[SERVER]\t Listening for UDP connections at {Configurator.SERVER_IP}:" +
              f"{Configurator.SERVER_UDP_PORT}...")

        while True:
            try:
                byte_data = sock.recvfrom(Configurator.BUFFER_SIZE)
                data_receive = byte_data[0].decode('utf-8')
                client_address = byte_data[1]

                if data_receive:
                    message_query = parse_string_msg(data_receive)

                    # print("\n-----")
                    # print("request: ", data_receive)

                    # message question
                    msg_question = message_query.question

                    # find in cache first
                    cached_record = self.CACHE.get(msg_question.qname, msg_question.qtype, msg_question.qclass)

                    if cached_record is not None:
                        # print("in cache")
                        message_result = Message(request=message_query)
                        message_result.add_a_new_record_to_answer_section(cached_record)
                    else:
                        message_result = self.handle_query(message_query)

                    # send back the result to resolver here
                    if not isinstance(message_result, str):
                        message_result = message_result.to_string()

                    response = message_result.encode('utf-8')

                    # print("response: ", message_result)
                    # print("-----\n")
                    sock.sendto(response, client_address)
            except Exception as e:
                print("An exception occurs while handling a udp connection. " + str(e))


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
