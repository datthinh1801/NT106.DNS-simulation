import sys
import argparse
import dns.query
import dns.zone
import dns.resolver
from colorama import Fore, Style

bracket = f"{Fore.BLUE}[{Fore.GREEN}*{Fore.BLUE}]{Style.RESET_ALL} "
bracket_err = f"{Fore.BLUE}[{Fore.RED}*{Fore.BLUE}]{Style.RESET_ALL} "
'''
parser = argparse.ArgumentParser()
parser.add_argument('domain')
args = parser.parse_args()
'''
# domain = (sys.argv[1])
domain = 'megacorpone.com'
#domain = 'zonetransfer.me'


def line():
    print('-' * 75)
    return None


def resolveDNS(system):
    resolver = dns.resolver.Resolver()
    results = resolver.query(system, "A")
    return results


def getNS():
    name_servers = dns.resolver.query(domain, 'NS')
    print("\nThe name servers for " + domain + " are:")
    line()
    for system in name_servers:
        A_records = resolveDNS(str(system))
        for item in A_records:
            answer = ','.join([str(item)])
        print(bracket, "{:30}".format(
            str(system).rstrip('.')), "{:15}".format(answer))
    return name_servers


def getMX():
    mail_server = dns.resolver.query(domain, 'MX')
    print("\nMail servers for", domain)
    line()
    for system in mail_server:
        A_records = resolveDNS(str(system.exchange))
        for item in A_records:
            answer = ','.join([str(item)])
        print(bracket, "{:30}".format(str(system.exchange).rstrip('.')), "{:15}".format(
            str(answer)), '\t', "{:5}".format("Preference:"), str(system.preference))
    return None


def zoneXFR():
    print("\nAttempting zone transfers for", domain,)

    for server in name_servers:
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(
                str(server).rstrip('.'), domain))
            print("\nResults for", server, "\nZone origin:",
                  str(zone.origin).rstrip('.'))
            line()
            for host in zone:
                if str(host) != '@':
                    A_records = resolveDNS(str(host) + "." + domain)
                    for item in A_records:
                        answer = ','.join([str(item)])
                    print(bracket, "{:30}".format(
                        str(host) + "." + domain), answer)
        except Exception as e:
            print("\nResults for", server, "\nZone origin:",
                  str(zone.origin).rstrip('.'))
            line()
            print(bracket_err,
                  f"{Fore.RED}Error:{Style.RESET_ALL}", e.__class__, e)


name_servers = getNS()
getMX()
zoneXFR()
print("\n")
