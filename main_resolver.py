import threading
import time

from Resolver import Resolver

try:
    resolver = Resolver()

    resolver_udp_thread = threading.Thread(target=resolver.start_listening_udp)
    resolver_udp_thread.start()
except KeyboardInterrupt:
    pass
