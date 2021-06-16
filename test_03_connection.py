from NameServer import NameServer
from Resolver import Resolver
from Database import Database
from configurator import Configurator
import socket
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ParseString import *
from AES import AESCipher


class NS(NameServer):
    def __init__(self):
        self.database = Database('testNS.db')

    def start_listening_tcp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (
            Configurator.OTHERS[0]['ip'], Configurator.OTHERS[0]['tcp'])

        print(f"[SERVER]\t Listening for TCP connections at {Configurator.OTHERS[0]['ip']}:" +
              f"{Configurator.OTHERS[0]['tcp']}...")

        sock.bind(server_address)
        sock.listen(0)

        connection, client_address = sock.accept()
        try:
            byte_data = connection.recv(Configurator.BUFFER_SIZE)
            data_receive = AESCipher().decrypt(byte_data)
            if data_receive:
                message_query = parse_string_msg(data_receive)

                print(
                    f"[SERVER]\t Receive request for {message_query.question.qname} via TCP")

                # message question
                msg_question = message_query.question

                # find in cache first
                cached_record = self.database.query_from_database(
                    msg_question.qname, msg_question.qtype, msg_question.qclass)

                if cached_record is not None:
                    message_result = Message(request=message_query)
                    message_result.add_a_new_record_to_answer_section(
                        cached_record)
                else:
                    message_result = self.handle_query(message_query)
                # send the result back to resolver here

                if not isinstance(message_result, str):
                    message_result = message_result.to_string()

                response = AESCipher().encrypt(message_result)
                connection.sendall(response)
        except Exception as e:
            pass
        finally:
            connection.close()
            return (data_receive, message_result)

    def start_listening_udp(self):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (
            Configurator.OTHERS[0]['ip'], Configurator.OTHERS[0]['udp'])

        sock.bind(server_address)
        print(f"[SERVER]\t Listening for UDP connections at {Configurator.OTHERS[0]['ip']}:" +
              f"{Configurator.OTHERS[0]['udp']}...")

        try:
            byte_data = sock.recvfrom(Configurator.BUFFER_SIZE)
            data_receive = AESCipher().decrypt(byte_data[0])
            client_address = byte_data[1]

            if data_receive:
                message_query = parse_string_msg(data_receive)

                print(
                    f"[SERVER]\t Receive request for {message_query.question.qname} via UDP")

                # message question
                msg_question = message_query.question

                # find in cache first
                cached_record = self.database.query_from_database(
                    msg_question.qname, msg_question.qtype, msg_question.qclass)

                if cached_record is not None:
                    # print("in cache")
                    message_result = Message(request=message_query)
                    message_result.add_a_new_record_to_answer_section(
                        cached_record)
                else:
                    message_result = self.handle_query(message_query)

                # send back the result to resolver here
                if not isinstance(message_result, str):
                    message_result = message_result.to_string()

                response = AESCipher().encrypt(message_result)

                sock.sendto(response, client_address)
        except Exception as e:
            print("An exception occurs while handling a udp connection. " + str(e))
        finally:
            return (data_receive, message_result)


class RS(Resolver):
    def __init__(self):
        self.database = Database('testRS.db')
        Configurator.IP = '127.0.0.1'
        Configurator.UDP_PORT = 9292
        Configurator.TCP_PORT = 9393

        Configurator.OTHERS.append(dict(ip='127.0.0.1', udp=5252, tcp=5353))
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

        print(f"[RESOLVER]\t Using TCP connections at {Configurator.IP}:" +
              f"{Configurator.TCP_PORT}...")

        tcp_resolver_socket.settimeout(1.0)
        tcp_resolver_socket.connect(server_address)

        try:
            bytes_to_send = AESCipher().encrypt(message)
            tcp_resolver_socket.sendall(bytes_to_send)

            # receiving data
            response = AESCipher().decrypt(tcp_resolver_socket.recv(
                Configurator.BUFFER_SIZE))
        except Exception as e:
            response = "Failed-" + str(e)
        finally:
            tcp_resolver_socket.close()
            return (message, response)

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

        print(f"[RESOLVER]\t Using UDP connections at {Configurator.IP}:" +
              f"{Configurator.UDP_PORT}...")

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
            return (message, response)


class TestConnection():
    import threading

    class ThreadWithResult(threading.Thread):
        def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
            def function():
                self.result = target(*args, **kwargs)
            super().__init__(group=group, target=function, name=name, daemon=daemon)

    def setup(self):
        self.rs = RS()
        self.ns = NS()

    def test_udp(self):
        header = MessageHeader()
        question = MessageQuestion('www.google.com', 1, 1)
        message = Message(header=header, question=question)
        plain_msg = message.to_string()

        thread1 = self.ThreadWithResult(target=self.ns.start_listening_udp)
        thread2 = self.ThreadWithResult(
            target=self.rs._use_udp, args=(plain_msg,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        assert thread1.result == thread2.result

    def test_tcp(self):
        header = MessageHeader()
        question = MessageQuestion('www.google.com', 1, 1)
        message = Message(header=header, question=question)
        plain_msg = message.to_string()

        thread1 = self.ThreadWithResult(target=self.ns.start_listening_tcp)
        thread2 = self.ThreadWithResult(
            target=self.rs._use_tcp, args=(plain_msg,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        assert thread1.result == thread2.result


if __name__ == '__main__':
    test_conn = TestConnection()
    test_conn.setup()
    test_conn.test_udp()
