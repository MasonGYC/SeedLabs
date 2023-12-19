#!/usr/bin/env python3

import fcntl
import struct
import os
import time
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'guo%d', IFF_TUN | IFF_NO_PI)
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

while True:
   # get a packet from the tun interface
   pkt = os.read(tun,2048)

   if pkt:
      ip = IP(pkt)
      print(ip.summary())
     
      # Send out a spoof packet using the tun interface
      # if this packet is echo-request, write a echo-reply
      if ICMP in ip:
         icmp = ip[ICMP]
         if icmp.type==8:
            # newpkt = IP(src=ip.dst,dst=ip.src)/ICMP()/"data"
            # os.write(tun,bytes(newpkt))
            newpkt = b"data"
            os.write(tun,newpkt)

