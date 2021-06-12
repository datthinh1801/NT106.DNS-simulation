#! /bin/python3

import scapy.all as scapy
from argparse import ArgumentParser


def parse_cli_args():
    """
    Parse arguments from CLI.
    """
    parser = ArgumentParser("ARP Spoofing Detector")
    parser.add_argument("-i", "--interface",
                        nargs='?',
                        default="eth0",
                        metavar="INTERFACE",
                        dest="interface",
                        help="the interface to sniff traffic from")
    return parser.parse_args()


def get_mac(target_ip):
    """Get MAC address of a given IP address."""
    # (Wikipedia) in an arp request, the hwdst field is ignored;
    # therefore, we need to create an Ether layer to carry the broadcast link-layer address
    arp_request = scapy.ARP(pdst=target_ip)
    ether = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast_packet = ether / arp_request

    # srp returns 2 lists
    # the first one contains pairs of request-response
    # the second one contains requests that are not responded

    # this function gets MAC address of one specific internet address;
    # therefore, there is only 1 answer in the response
    answer = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
    if answer:
        # get the response from the first and the only pair from the answer list
        return answer[0][1].hwdst
    else:
        return None


def sniff(interface):
    """
    Sniff packets from the given interface.
    """
    scapy.sniff(iface=interface, store=False, prn=process_packet)


def process_packet(packet):
    """
    Callback function to process sniffed packet.
    """
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        supposed_ip = packet[scapy.ARP].psrc
        supposed_mac = packet[scapy.ARP].hwsrc
        real_mac = get_mac(supposed_ip)

        if supposed_mac != real_mac:
            print(f"You are under attacks! The attacker might be at {supposed_mac} or {real_mac}")


args = parse_cli_args()
sniff(args.interface)