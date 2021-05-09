#! /bin/python3

import argparse

import scapy.all as scapy


def create_a_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", nargs="?", help="IP address of a target host or an IP range of a target network",
                        required=True)
    return parser.parse_args()


def scan(ip):
    # Create an ARP request
    arp_request = scapy.ARP(pdst=ip)


    # Create an Ethernet frame
    # Default value of dst is already 'ff:ff:ff:ff:ff:ff'
    ether = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

    # Combine arp_request and ether into a single packet
    broadcast_packet = ether / arp_request

    # Send the packet and capture responses
    return scapy.srp(broadcast_packet, timeout=1, verbose=False)[0]


def print_result(responses):
    print("IP\t\t\tMAC address")
    print("-" * 42)
    for response in responses:
        print(response[1].psrc, end="\t\t")
        print(response[1].hwsrc)


target = create_a_parser().target
answers = scan(target)
print_result(answers)
