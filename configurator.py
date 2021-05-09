import socket
import subprocess
import re
import os


class Configurator:
    """
    An abstract base class to config Resolver and Server settings.
    A note for using this. Do not create an object from this class. Use the class directly.
    For example, Configurator.SERVER_IP to access the SERVER_IP attribute.
    """
    RESOLVER_IP = ""
    RESOLVER_TCP_PORT = None
    RESOLVER_UDP_PORT = None

    SERVER_IP = ""
    SERVER_TCP_PORT = None
    SERVER_UDP_PORT = None

    BUFFER_SIZE = 4096

    @staticmethod
    def get_ip() -> str:
        """Extract ip from the local machine."""
        try:
            ifconfig_result = str(subprocess.check_output(["ifconfig", "eth0"]))
            match = re.search(r"inet \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", ifconfig_result)[0]
            return match.split(' ')[1]
        except:
            ipconfig_result = str(subprocess.check_output(["ipconfig"]))
            matches = re.findall(r"(?<=IPv4 Address. . . . . . . . . . . : )\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}",
                                 ipconfig_result)
            print("Select an ip from this list:")
            for i, ip in enumerate(matches):
                print(f"({i}) {ip}")
            return matches[int(input("Enter the index of the ip: "))]

    @staticmethod
    def config_server(tcp_port: int, udp_port: int):
        """Config server's constants."""
        print("##### SERVER CONFIG #####")
        Configurator.SERVER_IP = Configurator.get_ip()
        Configurator.SERVER_TCP_PORT = tcp_port
        Configurator.SERVER_UDP_PORT = udp_port
        try:
            os.system("cls")
        except:
            os.system("clear")

    @staticmethod
    def config_resolver(tcp_port: int, udp_port: int):
        """Config resolver's constants."""
        print("##### RESOLVER CONFIG #####")
        Configurator.RESOLVER_IP = Configurator.get_ip()
        Configurator.RESOLVER_TCP_PORT = tcp_port
        Configurator.RESOLVER_UDP_PORT = udp_port
        try:
            os.system("cls")
        except:
            os.system("clear")

    @staticmethod
    def set_buffer_size(size: int):
        if size > 0:
            Configurator.BUFFER_SIZE = size
