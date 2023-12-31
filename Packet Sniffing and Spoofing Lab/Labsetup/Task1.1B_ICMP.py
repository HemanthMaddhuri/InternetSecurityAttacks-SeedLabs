#/bin/env python3
from scapy.all import *

print("SNIFFING PACKETS........")

def print_pkt(pkt):
	if ICMP in pkt:
	    if pkt[ICMP].type == 0 or pkt[ICMP].type == 8: #from Berkley packet filter
        	print("Source IP:", pkt[IP].src)
        	print("Destination IP:", pkt[IP].dst)
        	print("Protocol:", pkt[IP].proto)
        	print("\n")
pkt = sniff(iface = 'br-a212141a7a0d', filter = 'icmp', prn = print_pkt)
