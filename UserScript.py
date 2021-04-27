"""
The client program is expected to pass arguments to this script directly.
Within 1 second, if a response is returned, the IP address of the queried
domain name will be written to an output file; otherwise, write out a "Timeout".
"""
import argparse
from socket import *
from constants import RESOLVER_ADDR


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
                        action='store',
                        nargs=1,
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
                        help='the type of the query',
                        metavar='QTYPE',
                        dest='qtype')

    # Add the third argument as the class type.
    # The value of this argument will be stored in the qclass variable
    # If no type is given, this will take the "IN" class by default
    parser.add_argument('-c', '--class',
                        nargs='?',
                        default='IN',
                        help='the class of the query',
                        metavar='QCLASS',
                        dest='qclass')
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
    msg = f"{args_obj.qname[0]};{args_obj.qtype};{args_obj.qclass}"
    # Send the message to the resolver
    client_socket.sendto(msg.encode(), RESOLVER_ADDR)
    # Extract the response only
    response = client_socket.recvfrom(1024)[0]
    client_socket.close()
    return response.decode() if response != None else None


args = parse_args()

# Catch socket.timeout exception
try:
    reponse = make_query(args)
except timeout:
    reponse = "Timeout"

# Write output to 'output.txt' file
with open('output.txt', 'w') as f:
    f.write(reponse)
