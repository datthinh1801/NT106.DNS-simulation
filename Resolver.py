import socket
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ResourceRecord import ResourceRecord
from ParseString import parse_string_msg
from CacheSystem import CacheSystem
from configurator import Configurator
from ParseString import parse_string_cachesystem
from ParseString import parse_string_question


class Resolver:
    def __init__(self):
        """Initialize a Resolver."""
        self.cache_system = CacheSystem()
        Configurator.config_resolver(9393, 9292)
        Configurator.SERVER_IP = input('Enter IP of NameServer: ')
        Configurator.BACKUP_SERVER_IP = input('Enter IP of BackUp NameServer: ')

        # Update cache from local file
        try:
            # open the local cache file to load past caches
            with open("CacheSystem.txt", "r") as f:
                self.cache_system = parse_string_cachesystem(f.read())
        except:
            # if a local file does not exist, which means there is no past cache,
            # do nothing
            pass

    @staticmethod
    def _use_tcp(message: str) -> str:
        """
        Create a TCP connection to server, then send the message.
        If there is an error while sending and receiving the message, an exception will be returned.
        """
        tcp_resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (Configurator.SERVER_IP, Configurator.SERVER_TCP_PORT)
        tcp_resolver_socket.settimeout(1.0)
        tcp_resolver_socket.connect(server_address)

        try:
            # Sending data
            bytes_to_send = message.encode('utf-8')
            tcp_resolver_socket.sendall(bytes_to_send)

            # receiving data
            response = tcp_resolver_socket.recv(Configurator.BUFFER_SIZE).decode('utf-8')
        except Exception as e:
            response = "Failed-" + str(e)
        finally:
            tcp_resolver_socket.close()
            return response

    @staticmethod
    def _use_udp(message: str) -> str:
        """
        Create a UDP connection to server, then send the message.
        If there is an error while sending and receiving the message, an exception will be returned.
        """
        bytes_to_send = message.encode('utf-8')
        server_address = (Configurator.SERVER_IP, Configurator.SERVER_UDP_PORT)

        # Create a UDP socket at client side
        udp_resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_resolver_socket.settimeout(1.0)

        try:
            # Send data
            udp_resolver_socket.sendto(bytes_to_send, server_address)

            # Receiving data & convert bytes of data to a string
            response = udp_resolver_socket.recvfrom(Configurator.BUFFER_SIZE)[0].decode('utf-8')
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
        # Check the cache database for existing answer record
        cached_record = self.cache_system.get(name=request.question.qname + ".", rr_type=request.question.qtype,
                                              rr_class=request.question.qclass)

        # If an answer record for the query is already cached,
        # return the record
        if cached_record is not None:
            return cached_record.to_string()

        # Otherwise, send the query to the NameServer
        if tcp:
            response = self._use_tcp(request.to_string())
        else:
            response = self._use_udp(request.to_string())

        if response.split("-")[0] == "Failed":
            return response.split("-")[1]
        else:
            message_answer = parse_string_msg(response)

        # save to on-memory cache system
        self.save_to_cache_system(message_answer)
        # write new database to file
        self.save_to_database()

        # return the first resource record in the answer section
        first_rr = message_answer.answers[0]
        return first_rr.to_string()

    def save_to_cache_system(self, message_response: Message):
        """
        Cache resource record from a Message object.
        """
        for answer in message_response.answers:
            self.cache_system.put(answer)

        for authority in message_response.authorities:
            self.cache_system.put(authority)

        for add in message_response.additional:
            self.cache_system.put(add)

    def save_to_database(self):
        """
        Save cache to a local file.
        """
        with open("CacheSystem.txt", "w") as f:
            data = self.cache_system.to_string()
            f.write(data)

    def start_listening_udp(self):
        """
        Listen to incoming connections from clients to resolve requests in-house.
        """
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener_socket.bind((Configurator.RESOLVER_IP, Configurator.RESOLVER_UDP_PORT))
        print(
            f"[RESOLVER]\t Listening for clients' requests at {Configurator.RESOLVER_IP}:" +
            f"{Configurator.RESOLVER_UDP_PORT}...")

        while True:
            # Receive an incoming request
            byte_data = listener_socket.recvfrom(Configurator.BUFFER_SIZE)
            client_address = byte_data[1]
            request = byte_data[0].decode('utf-8').split(';')
            protocol = request.pop()
            request = ';'.join(request)

            print(f"[RESOLVER]\t Receive a request for {request} from {client_address} using {protocol.upper()}")

            # Handle the request and create a Message object for further query
            response = ""
            try:
                question = parse_string_question(request)
            except Exception as e:
                response = "[EXCEPTION] " + str(e)

            if response == "" :
                header = MessageHeader()
                request_message = Message(header=header, question=question)
                if protocol == 'udp':
                    response = self.query(request=request_message, tcp=False)
                else:
                    response = self.query(request=request_message, tcp=True)

            try:
                listener_socket.sendto(response.encode('utf-8'), client_address)
            except:
                continue
