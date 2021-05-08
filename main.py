import threading
import time

from Resolver import Resolver
from NameServer import NameServer
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from Message import Message

resolver = Resolver()
name_server = NameServer()

server_udp_thread = threading.Thread(target=name_server.start_listening_udp, args=())
server_udp_thread.start()

server_tcp_thread = threading.Thread(target=name_server.start_listening_tcp, args=())
server_tcp_thread.start()

time.sleep(1)
while True:
    try:
        header = MessageHeader(qr=0, rd=True, ra=True)
        domain_to_resolve = input("Enter a domain name to resolve: ")
        question = MessageQuestion(domain_to_resolve, 1, 1)
        message = Message(question=question, header=header)
        message_str = message.to_string()
        print("Message:")
        print(message_str)

        rr_udp = resolver.query(message=message_str, tcp=False)
        print(f"Result from UDP: {rr_udp}")
        rr_tcp = resolver.query(message=message_str, tcp=True)
        print(f"Result from TCP: {rr_tcp}")
        print('-' * 30)
    except KeyboardInterrupt:
        print("Quitting...")
        break
