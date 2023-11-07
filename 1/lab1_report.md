Lab 1: Packet Sniffing and Spoofing
Name: Guo Yuchen
Student ID: 1004885
Task 1.1A
What I have done
Setup: Starting the containers using `dcup`

Using ifconfig to get network interface ID br-e6512860ed72



Create a Python file `sniffer.py` and make it executable using `chmod a+x sniffer.py`.
The code is as follows:




Running sniffer.py with root privilege:
Using `nc` command on 10.9.0.5 to listen to the connection from 10.9.0.6

Traffic captured by Scapy:


Running sniffer.py without root privilege:



Observation:
Only root privilege can run sniffer.py

Explanation
?
Important Code snippet:
```
#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

pkt = sniff(iface="br-e6512860ed72", prn=print_pkt)
```
Task 1.1B
What I have done

Capture only the ICMP packet
```
#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

pkt = sniff(iface="br-e6512860ed72", filter="icmp", prn=print_pkt)
```


• Capture any TCP packet that comes from a particular IP and with a destination port number 23.

```
#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

pkt = sniff(iface="br-e6512860ed72", filter="tcp and src net 10.9.0.5 and dst port 23",prn=print_pkt)
```


It only responds when the port number, src ip, and packet type fit the filter.

• Capture packets comes from or to go to a particular subnet. 
```
#!/usr/bin/env python3
from scapy.all import *

def print_pkt(pkt):
	pkt.show()

pkt = sniff(iface="br-e6512860ed72", filter="net 128.230.0.0/16",prn=print_pkt)
```










Observation:


Explanation
?
Important Code snippet:



Task 1.2
icmpSpoofer.py:
```
#!/usr/bin/env python3
from scapy.all import *
a = IP()
a.src = "6.6.6.6"
a.dst = "10.9.0.6"
b = ICMP()
p = a/b 
send(p)
```



Task 1.3


Task 1.4
```
#!/usr/bin/env python3
from scapy.all import *

def spoof_pkt(pkt):
	src = pkt[IP].dst
	dst = pkt[IP].src
	a = IP(src=src,dst=dst,ttl=40)
	send(a/ICMP())

pkt = sniff(iface="br-e6512860ed72", filter="icmp and host 10.9.0.5",prn=spoof_pkt)
```
1.2.3.4




10.9.0.99



8.8.8.8


