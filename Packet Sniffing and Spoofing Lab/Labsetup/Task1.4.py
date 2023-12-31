#!/usr/bin/python

from scapy.all import *

def sniff_spoof(pkt):
    if pkt[ICMP].type == 8:
        print("Received ICMP Echo Request")
        a = IP(src = pkt[IP].dst, dst = pkt[IP].src)
        b = ICMP(type = 0, id = pkt[ICMP].id, seq = pkt[ICMP].seq) #using type, id and sequence parameters
        p = a / b / pkt[3].load   #pkt is printed as array in my observation so I went on used pkt[3].load which means raw object of packet
        send(p)
        print("Spoofed ICMP Echo Reply Sent")
pkt = sniff(iface = ['br-a212141a7a0d', 'enp0s3'],filter="icmp", prn=sniff_spoof)
