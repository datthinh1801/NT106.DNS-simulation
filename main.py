import threading
import time

from Resolver import Resolver
from NameServer import NameServer
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from Message import Message

try:
    resolver = Resolver()
    name_server = NameServer()

    server_udp_thread = threading.Thread(target=name_server.start_listening_udp)
    server_udp_thread.start()

    server_tcp_thread = threading.Thread(target=name_server.start_listening_tcp)
    server_tcp_thread.start()

    resolver_udp_thread = threading.Thread(target=resolver.start_listening_udp)
    resolver_udp_thread.start()
except KeyboardInterrupt:
    pass
