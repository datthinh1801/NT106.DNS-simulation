import socket
import threading
from Message import Message
from AES import AESCipher
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ResourceRecord import ResourceRecord
from ParseString import parse_string_msg
from configurator import Configurator
from ParseString import parse_string_question
from Database import Database


class Resolver:
    def __init__(self):
        """Initialize a Resolver."""
        self.database = Database('DatabaseResolver.db')
        Configurator.config_me(9292, 9393)
        Configurator.config_others(int(input("Number of name servers: ")))
        self.this_ns_idx = 0

    def _use_tcp(self, message: str) -> str:
        """
        Create a TCP connection to server, then send the message.
        If there is an error while sending and receiving the message, an exception will be returned.
        """
        tcp_resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (
            Configurator.OTHERS[self.this_ns_idx]['ip'], Configurator.OTHERS[self.this_ns_idx]['tcp'])
        self.this_ns_idx = (self.this_ns_idx + 1) % len(Configurator.OTHERS)

        tcp_resolver_socket.settimeout(1.0)
        tcp_resolver_socket.connect(server_address)

        try:
            # Sending data

            # encrypt the message before send to server
            bytes_to_send = AESCipher().encrypt(message)
            tcp_resolver_socket.sendall(bytes_to_send)

            # receiving data
            response = AESCipher().decrypt(tcp_resolver_socket.recv(
                Configurator.BUFFER_SIZE))
        except Exception as e:
            response = "Failed-" + str(e)
        finally:
            tcp_resolver_socket.close()
            return response

    def _use_udp(self, message: str) -> str:
        """
        Create a UDP connection to server, then send the message.
        If there is an error while sending and receiving the message, an exception will be returned.
        """

        # encrypt the message before send to server
        bytes_to_send = AESCipher().encrypt(message)
        server_address = (
            Configurator.OTHERS[self.this_ns_idx]['ip'], Configurator.OTHERS[self.this_ns_idx]['udp'])
        self.this_ns_idx = (self.this_ns_idx + 1) % len(Configurator.OTHERS)

        # Create a UDP socket at client side
        udp_resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_resolver_socket.settimeout(1.0)

        try:
            # Send data
            udp_resolver_socket.sendto(bytes_to_send, server_address)

            # Receiving data & convert bytes of data to a string
            # decrypt receive message
            response = AESCipher().decrypt(udp_resolver_socket.recvfrom(
                Configurator.BUFFER_SIZE)[0])
        except Exception as e:
            response = "Failed-" + str(e)
        finally:
            udp_resolver_socket.close()
            return response

    def query(self, request: Message, tcp: bool = False) -> str:
        """
        Resolve the request.
        Before asking the name server, resolver will check its cache system for cached resource records.
        """
        # Search in database
        self.database.refresh()
        cache_record = self.database.query_from_database(request.question.qname + ".", request.question.qtype,
                                        request.question.qclass)
        
        if cache_record is not None:
            return cache_record.to_string()

        # Otherwise, send the query to the NameServer
        if tcp:
            response = self._use_tcp(request.to_string())
        else:
            response = self._use_udp(request.to_string())

        if response.split("-")[0] == "Failed":
            return response.split("-")[1]
        else:
            message_answer = parse_string_msg(response)
        self.save_to_database(message_answer)

        # return the first resource record in the answer section
        first_rr = message_answer.answers[0]
        return first_rr.to_string()

    def save_to_database(self, message_response: Message):
        for answer in message_response.answers:
            self.database.add_to_database(answer)

        for authority in message_response.authorities:
            self.database.add_to_database(authority)

        for add in message_response.additional:
            self.database.add_to_database(add)

    def start_listening_udp(self):
        """
        Listen to incoming connections from clients to resolve requests in-house.
        """
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener_socket.bind(
            (Configurator.IP, Configurator.UDP_PORT))
        print(
            f"[RESOLVER]\t Listening for clients' requests at {Configurator.IP}:" +
            f"{Configurator.UDP_PORT}...")

        while True:
            # Receive an incoming request
            byte_data = listener_socket.recvfrom(Configurator.BUFFER_SIZE)
            client_address = byte_data[1]
            request = byte_data[0].decode('utf-8').split('\n')
            #print('request:',request)
            if request[0] == 'encrypted':
                request = AESCipher().decrypt(request[1]).split(';')
            else:
                request = request[1].split(';')
            protocol = request.pop()
            request = ';'.join(request)

            print(
                f"[RESOLVER]\t Receive a request for {request} from {client_address} using {protocol.upper()}")

            # Handle the request and create a Message object for further query
            response = ""
            try:
                question = parse_string_question(request)
            except Exception as e:
                response = "[EXCEPTION] " + str(e)

            if response == "":
                header = MessageHeader()
                request_message = Message(header=header, question=question)
                if protocol.lower() == 'udp':
                    response = self.query(request=request_message, tcp=False)
                else:
                    response = self.query(request=request_message, tcp=True)

            try:
                listener_socket.sendto(
                    response.encode('utf-8'), client_address)
            except:
                continue


if __name__ == '__main__':
    try:
        resolver = Resolver()

        udp_thread = threading.Thread(target=resolver.start_listening_udp)
        udp_thread.start()
    except KeyboardInterrupt:
        pass
