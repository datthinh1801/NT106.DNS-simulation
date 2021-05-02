import constants
import socket


def config_server(tcp_port: int, udp_port: int):
    """Config server's constants."""
    constants.SERVER_IP = socket.gethostbyname(socket.gethostname())
    constants.SERVER_TCP_PORT = tcp_port
    constants.SERVER_UDP_PORT = udp_port


def config_resolver(tcp_port: int, udp_port: int):
    """Config server's constants."""
    constants.RESOLVER_IP = socket.gethostbyname(socket.gethostname())
    constants.RESOLVER_TCP_PORT = tcp_port
    constants.RESOLVER_UDP_PORT = udp_port
