import socket


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

    def __init__(self):
        pass

    @staticmethod
    def config_server(tcp_port: int, udp_port: int):
        """Config server's constants."""
        Configurator.SERVER_IP = socket.gethostbyname(socket.gethostname())
        Configurator.SERVER_TCP_PORT = tcp_port
        Configurator.SERVER_UDP_PORT = udp_port

    @staticmethod
    def config_resolver(tcp_port: int, udp_port: int):
        """Config resolver's constants."""
        Configurator.RESOLVER_IP = socket.gethostbyname(socket.gethostname())
        Configurator.RESOLVER_TCP_PORT = tcp_port
        Configurator.RESOLVER_UDP_PORT = udp_port

    @staticmethod
    def set_buffer_size(size: int):
        if size > 0:
            Configurator.BUFFER_SIZE = size
