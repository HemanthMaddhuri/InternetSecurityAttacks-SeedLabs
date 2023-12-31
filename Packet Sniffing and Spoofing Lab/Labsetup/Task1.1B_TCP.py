#/bin/env python3
from scapy.all import *

print("SNIFFING PACKETS........")

def print_pkt(pkt):
    if TCP in pkt:
        print("Source IP: ", pkt[IP].src)
        print("Destination IP: ", pkt[IP].dst)
        print("TCP Source port: ", pkt[TCP].sport)
        print("TCP Destination port: ", pkt[TCP].dport)
        print("\n")
pkt = sniff(iface = 'br-a212141a7a0d', filter = 'tcp dst port 23 and src host 10.9.0.5 ', prn = print_pkt)
