# Resolver class definition
from socket import *
from Message import *


class Resolver:
    def __init__(self):
        """Initialize a DNS resolver."""
        self.server_host = "192.168.100.4"
        self.server_port = 5353
        self.server_addr = (self.server_host, self.server_port)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(self.server_addr)

    def activate(self) -> None:
        """Main routine of the resolver."""
        print("[INFO] Server is up and listening...")

        while True:
            raw_data, client_addr = self.server_socket.recvfrom(4096)
            requesting_hostname = raw_data.decode()

            if self._search_for_cache(requesting_hostname) == "":
                request = Message(requesting_hostname)
                response = self._forward_dns_request(request)
                self._add_new_entry_to_cache(response)
                self._return_response_to_user(response.getIP(), client_addr)
            else:
                pass
            pass

        self.server_socket.close()

    def _forward_dns_request(self, request: Message) -> Message:
        """Send a DNS request to a name server and return the response."""
        ip = Message()
        return ip

    def _parse_dns_response(self, response: Message) -> str:
        """Parse a DNS response to extract the IP address and return that IP."""
        pass

    def _search_for_cache(self, requesting_host: str) -> str:
        return ""

    def _add_new_entry_to_cache(self, entry: Message) -> None:
        pass

    def _return_response_to_user(self, returned_ip: str, client_addr: tuple) -> None:
        pass


r = Resolver()
r.activate()
