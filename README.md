# DNS simulation
<a href="https://www.uit.edu.vn/">
<p align="center">
  <img width="300" height="250" src="https://user-images.githubusercontent.com/44528004/122157620-5b2c2200-ce95-11eb-9b6c-8df62f5d282a.png">
</p>
</a>

<p align="center">
  <img src="https://github.com/datthinh1801/NT106.DNS-simulation/actions/workflows/python-dependencies.yml/badge.svg">
  <img src="https://github.com/datthinh1801/NT106.DNS-simulation/actions/workflows/flake8.yml/badge.svg">
  <img src="https://github.com/datthinh1801/NT106.DNS-simulation/actions/workflows/pytest.yml/badge.svg">
</p>
<p align="center">
  <img src="https://www.codefactor.io/repository/github/datthinh1801/nt106.dns-simulation/badge">
  <a href="https://www.codacy.com/gh/datthinh1801/NT106.DNS-simulation/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=datthinh1801/NT106.DNS-simulation&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/3be6c6100d694b888dc5cfe1e9039f47"/></a>
 </p>

This project is part of a university curriculum which is *Basic Networking Programming*.  

# Introduction
This project has 3 main features.  
1. Simulate DNS protocol  
2. Demonstrate a Man-In-The-Middle attack to poison DNS reponses from the **Resolver** to the **User**, this is called **DNS poisoning**.
3. Demonstrate some mitigations.

## Dependencies
- `scapy` (for python 3.9)
- `dnspython` (for python 3.9)
- `netfilterqueue` (for python 2.7)

# Instruction
## DNS protocol simulation
### Nameserver
To run the Nameserver, just execute the following command:  
```
python3 NameServer.py
```  
> If you are using Windows, you might be asked to select an IP address that the NameServer will bind to.  

If the script is executed successfully, you will see this:  
```
[SERVER]         Listening for UDP connections at 10.0.0.10:5252...
[SERVER]         Listening for TCP connections at 10.0.0.10:5353...
```

### Resolver
To run the Resolver, execute the following command:
```
python3 Resolver.py
```  
> If you are using Windows, you might be asked to select an IP address that the NameServer will bind to.  
> Also, you'll be asked to enter the number of nameservers with their corresponding IP addresses that this resolver will connect to.  

If the script is executed successfully, you will see this:  
```
[RESOLVER]       Listening for clients' requests at 10.0.0.7:9292...
```

### User
In order for the **User** to make a query, run the `UserScript.py`.  
For more information, execute the script with `-h` option (`python3 UserScript.py -h`).  
```python
usage: UserScript.py [-h] -d [QNAME] [-t [QTYPE]] [-c [QCLASS]] --ip [IP] --port [PORT] [--protocol [PROTOCOL]] [--secure [SECURE]]

Parse DNS arguments from CLI

optional arguments:
  -h, --help            show this help message and exit
  -d [QNAME], --domain [QNAME]
                        the domain name to be queried
  -t [QTYPE], --type [QTYPE]
                        the type of the query (A by default)
  -c [QCLASS], --class [QCLASS]
                        the class of the query (IN by default)
  --ip [IP]             IP address of the resolver
  --port [PORT]         port number that the resolver is listening
  --protocol [PROTOCOL]
                        tcp/udp (udp by default)
  --secure [SECURE]     1/0 secure connection with encrypted query payload (encrypted by default)
```  

Example:  
```
python3 -d facebook.com --ip 10.0.0.10 --port 9292 --protocol tcp --secure 0
```

## DNS Poisoning
### Network Scanner
To be the man in the middle, you need to know the IP addresses of our 2 targets. For this reason, run the `Network_Scanner.py` script with the `-t` option to specify the IP range of the network that you want to scan.  
The outcome of this script will be the ***IP addresses*** as well as ***MAC addresses*** of **all hosts** in the targeted network.  
Use the `-h` option to see the help message.
```python
usage: Network_Scanner.py [-h] -t [TARGET]

optional arguments:
  -h, --help            show this help message and exit
  -t [TARGET], --target [TARGET]
                        IP address of a target host or an IP range of a target network
```  
Example:  
```
python3 Network_Scanner.py -t 10.0.0.0/24
```  

### ARP Spoofer
After having the IP addresses of your targets, run the `ARP_spoofer.py` script and specify the IP addresses of our 2 targets to start spoofing them. This spoof takes advantages of **ARP** to deceive both targets.  
For more information, use the `-h` option to see the help message.
```python
usage: ARP spoofer [-h] -t TARGET_IP -g GATEWAY_IP

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_IP, --target TARGET_IP
                        the IP address of the target machine
  -g GATEWAY_IP, --gateway GATEWAY_IP
                        the IP address of the default gateway
```  
> Originally, this tool was developed to spoof a host and a default gateway. However, this can be run to spoof 2 arbitrary hosts on the same network. If that is the case, we can use `-t` and `-g` interchangeably to specify our 2 targets.  

Example (you might be asked to run with privileged permissions):  
```
python3 ARP_spoofer.py -t 10.0.0.5 -t 10.0.0.7
```  

If the script is executed successfully, the followwing output will be printed:  
```
[+] Spoofed ['10.0.0.7'] and ['10.0.0.5'] successfully!
```

### DNS Poisoner
Once we become the man in the middle, we can run `DNS_poisoner.py` to poison DNS response from Resolver to User.  
For more information, use the `-h` option to see the help message.
```python
usage: DNS poisoner [-h] -t TARGET DOMAIN [TARGET DOMAIN ...] -d
                   [DESTINATION IP ADDRESS] [-l [TRUE]]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET DOMAIN [TARGET DOMAIN ...], --target-domains TARGET DOMAIN [TARGET DOMAIN ...]
                        Domain names that we want to poison
  -d [DESTINATION IP ADDRESS], --destined-domain [DESTINATION IP ADDRESS]
                        Our evil IP address that we want the victim to reach
  -l [TRUE], --local [TRUE]
                        Use this option if this script is run locally
```  

Example (you might be asked to run with privileged permissions):
```
python DNS_poisoner.py -t facebook.com google.com -d 10.0.0.10
```  
> This script must by run with **Python 2**.

### DNS Poisoning Detector
The detector authenticates each ARP response. More specifically, anytime the host running the detector receives an ARP response with an IP address `X` and a MAC address `M`, it will immediately broadcast an ARP request to ask which host has the IP address `X`. If the response to that request having the same MAC address `M`, we're not being under an attack; otherwise, we are.  

For more information, use the `-h` option to the help message.  
```python
sage: ARP Spoofing Detector [-h] [-i [INTERFACE]]

optional arguments:
  -h, --help            show this help message and exit
  -i [INTERFACE], --interface [INTERFACE]
                        the interface to sniff traffic from
```  

Example:  
```
python3 ARP_spoofing_detector.py -i eth0
```  

The output of this script will be the potential MAC address of the attacker.  

### Cryptography
ARP Spoofing Detector will detect an ARP spoofing attack. Meanwhile, cryptography plays an important role in preventing the attack.  

In the `UserScript.py`, if you run the script with the `--secure 1` option, the payload will be transmitted in encrypted form (this is the default behavior). Therefore, if the attacker does not have the key, he can't poison our reponse.  
On the other hand, to demonstrate the ARP Spoofing Detector, we also provide the option `--secure 0`, in which the payload will not be encrypted before being transmitted.

# Contributors
<a href="https://github.com/datthinh1801/NT106.DNS-simulation/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=datthinh1801/NT106.DNS-simulation" />
</a>

Made with [contributors-img](https://contrib.rocks).
