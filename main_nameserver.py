import threading
import time

from NameServer import NameServer

try:
    name_server = NameServer()

    server_udp_thread = threading.Thread(target=name_server.start_listening_udp)
    server_udp_thread.start()

    server_tcp_thread = threading.Thread(target=name_server.start_listening_tcp)
    server_tcp_thread.start()
except KeyboardInterrupt:
    pass