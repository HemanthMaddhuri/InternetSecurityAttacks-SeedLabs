from scapy.all import*

a = IP()
a.src = '1.2.3.4'
a.dst = '10.9.0.6'
b = ICMP()
p = a/b
send(p)
