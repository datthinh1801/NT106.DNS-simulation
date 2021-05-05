import socket
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ResourceRecord import ResourceRecord
from ParseString import parse_string_msg
from CacheSystem import CacheSystem
from configurator import Configurator


class Resolver:
    def __init__(self):
        """Initialize a Resolver."""
        self.cache_system = CacheSystem()
        Configurator.config_resolver(9393, 9292)

    @staticmethod
    def use_tcp(message: str) -> str:
        """
        Create a TCP connection to server, then send the message.
        If there is an error while sending and receiving the message, an exception will be returned.
        """
        tcp_resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (Configurator.SERVER_IP, Configurator.SERVER_TCP_PORT)
        tcp_resolver_socket.connect(server_address)

        try:
            # Sending data
            bytes_to_send = message.encode('utf-8')
            tcp_resolver_socket.sendall(bytes_to_send)

            # receiving data
            response = tcp_resolver_socket.recv(Configurator.BUFFER_SIZE).decode('utf-8')
        except Exception as e:
            response = str(e)
        finally:
            tcp_resolver_socket.close()
            return response

    @staticmethod
    def use_udp(message: str) -> str:
        """
        Create a UDP connection to server, then send the message.
        If there is an error while sending and receiving the message, an exception will be returned.
        """
        bytes_to_send = message.encode('utf-8')
        server_address = (Configurator.SERVER_IP, Configurator.SERVER_UDP_PORT)

        # Create a UDP socket at client side
        udp_resolver_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        try:
            # Send data
            udp_resolver_socket.sendto(bytes_to_send, server_address)

            # Receiving data & convert bytes of data to a string
            response = udp_resolver_socket.recvfrom(Configurator.BUFFER_SIZE)[0].decode('utf-8')
        except Exception as e:
            response = str(e)
        finally:
            udp_resolver_socket.close()
            return response

    def query(self, message: str, tcp: bool = False) -> str:
        # Create a Message query from a given string message
        message_query = parse_string_msg(message)
        message_question = message_query.question

        cached_record = self.cache_system.get(name=message_question.qname, rr_type=message_question.qtype,
                                              rr_class=message_question.qclass)
        # If an answer record for the query is already cached,
        # return the record
        if cached_record is not None:
            # print("in cache")
            return cached_record.to_string()

        # Otherwise, send the query to the NameServer
        request = message
        response = None
        while response is None:
            if tcp:
                response = self.use_tcp(request)
            else:
                response = self.use_udp(request)

        if response.split("-")[0] == "Failed":
            return response.split("-")[1]
        else:
            message_answer = parse_string_msg(response)

        # save to cache
        self.save_to_cache_system(message_answer)

        first_rr = message_answer.answers[0]
        return first_rr.to_string()

    def save_to_cache_system(self, message_response: Message):
        for answer in message_response.answers:
            self.cache_system.put(answer)

        for authority in message_response.authorities:
            self.cache_system.put(authority)

        for add in message_response.additional:
            self.cache_system.put(add)
