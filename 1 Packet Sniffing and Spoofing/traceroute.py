#!/usr/bin/env python3
from scapy.all import *
for ttl in range(1,30):
	pkt = IP(dst = "1.2.3.4",ttl = ttl)/ICMP()
	send(pkt)
