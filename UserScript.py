"""
The client program is expected to pass arguments to this script directly.
Within 1 second, if a response is returned, the IP address of the queried
domain name will be written to an output file; otherwise, write out a "Timeout".
"""
import argparse
from socket import *
from configurator import Configurator
from MessageQuestion import MessageQuestion


def parse_args():
    """
    Parse arguments from the command-line string.

    Arguments:
    -n, --domain    : the domain name to be queried [required]
    -t, --type      : the type of the query         ["A" by default]
    -c, --class     : the class of the query        ["IN" by default]
    """
    # Initialize a parser object
    parser = argparse.ArgumentParser(
        description="Parse DNS arguments from CLI", argument_default=None)

    # Add the first argument as the domain name.
    # The value of this argument will be stored in the qname variable.
    parser.add_argument('-d', '--domain',
                        nargs='?',
                        required=True,
                        help='the domain name to be queried',
                        metavar='QNAME',
                        dest='qname')

    # Add the second argument as the query type.
    # The value of this argument will be stored in the qtype variable
    # If no type is given, this will take the "A" type by default
    parser.add_argument('-t', '--type',
                        nargs='?',
                        default='A',
                        help='the type of the query (A by default)',
                        metavar='QTYPE',
                        dest='qtype')

    # Add the third argument as the class type.
    # The value of this argument will be stored in the qclass variable
    # If no type is given, this will take the "IN" class by default
    parser.add_argument('-c', '--class',
                        nargs='?',
                        default='IN',
                        help='the class of the query (IN by default)',
                        metavar='QCLASS',
                        dest='qclass')
    parser.add_argument('--ip',
                        nargs='?',
                        required=True,
                        help='IP address of the resolver',
                        metavar='IP',
                        dest='resolver_ip')
    parser.add_argument('--port',
                        nargs='?',
                        required=True,
                        help='port number that the resolver is listening',
                        metavar='PORT',
                        dest='resolver_port',
                        type=int)
    parser.add_argument('--protocol',
                        nargs='?',
                        default='udp',
                        help='tcp/udp (udp by default)',
                        dest='protocol',
                        type=str)
    return parser.parse_args()


def make_query(args_obj) -> str:
    """
    Create a socket and send a query to resolver.
    Return the inquired IP address (if any); otherwise None.
    """
    # Create a socket for client program
    client_socket = socket(AF_INET, SOCK_DGRAM)
    # Set timeout for 1 second
    client_socket.settimeout(1.0)

    # Prepare a message for transmission
    # msg = f"{args_obj.qname};{args_obj.qtype};{args_obj.qclass};{args_obj.protocol}"
    # --------------------------
    qst = MessageQuestion(args_obj.qname, args_obj.qtype, args_obj.qclass)
    msg = qst.to_string()+";"+args_obj.protocol
    # Send the message to the resolver
    resolver_address = (args_obj.resolver_ip, args_obj.resolver_port)
    client_socket.sendto(msg.encode(), resolver_address)

    # Extract the response only
    response = client_socket.recvfrom(1024)[0]
    client_socket.close()
    return response.decode() if response is not None else None


args = parse_args()

# Catch socket.timeout exception
try:
    response = make_query(args)
except timeout:
    response = "[EXCEPTION] Timeout"
except Exception as e:
    response = "[EXCEPTION] " + str(e)
finally:
    print(response)
