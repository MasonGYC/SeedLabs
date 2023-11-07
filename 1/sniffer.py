#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

'''Task 1.1A ''' 
# pkt = sniff(iface="br-e6512860ed72", prn=print_pkt)

'''Task 1.1B ''' 
# pkt = sniff(iface="br-e6512860ed72", filter="icmp", prn=print_pkt)
# pkt = sniff(iface="br-e6512860ed72", filter="tcp and src net 10.9.0.5 and dst port 23",prn=print_pkt)
# pkt = sniff(iface="br-e6512860ed72", filter="net 128.230.0.0/16",prn=print_pkt)




