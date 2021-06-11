import subprocess
import re
import os


class Configurator:
    """
    An abstract base class to config Resolver and Server settings.
    A note for using this. Do not create an object from this class. Use the class directly.
    For example, Configurator.SERVER_IP to access the SERVER_IP attribute.
    """
    IP = ""
    TCP_PORT = None
    UDP_PORT = None

    OTHERS = []

    BUFFER_SIZE = 4096

    @staticmethod
    def get_ip() -> str:
        """Extract ip from the local machine."""
        try:
            ifconfig_result = str(
                subprocess.check_output(["ifconfig", "eth0"]))
            match = re.search(
                r"inet \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", ifconfig_result)[0]
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
    def config_me(udp_port: int, tcp_port: int):
        """Config socket's constants."""
        print("##### SOCKET CONFIG #####")
        Configurator.IP = Configurator.get_ip()
        Configurator.TCP_PORT = tcp_port
        Configurator.UDP_PORT = udp_port
        os.system("clear")

    @staticmethod
    def config_others(num_partners: int):
        """Config others socket's constants."""
        print("##### SOCKET CONFIG #####")
        for _ in range(num_partners):
            ip = input("IP: ")
            udp_port = int(input("UDP port number: "))
            tcp_port = int(input("TCP port number: "))
            Configurator.OTHERS.append(dict(ip=ip, udp=udp_port, tcp=tcp_port))
        os.system("clear")
        assert num_partners == len(Configurator.OTHERS)

    @staticmethod
    def set_buffer_size(size: int):
        if size > 0:
            Configurator.BUFFER_SIZE = size
