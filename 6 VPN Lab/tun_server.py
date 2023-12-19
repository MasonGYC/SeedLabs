#!/usr/bin/env python3
from scapy.all import*
import fcntl
import struct
import os
import time
from scapy.all import *

IP_A = "0.0.0.0"
PORT = 9090
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

# task 4: 
# Create a TUN interface and configure it.
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'guo%d', IFF_TUN | IFF_NO_PI)
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

os.system("ip addr add 192.168.53.5/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

# while True:
#     # task 3:
#     # data, (ip, port) = sock.recvfrom(2048)
#     # print("{}:{} --> {}:{}".format(ip, port, IP_A, PORT))
#     # pkt = IP(data)
#     # print("   Inside: {} --> {}".format(pkt.src, pkt.dst))


#     # task 4:
#     # Get the data from the socket interface; treat the received data as an IP packet.
#     data, (ip, port) = sock.recvfrom(2048)
#     pkt = IP(data)
#     print(pkt.summary())

#     # Write the packet to the TUN interface.
#     os.write(tun,bytes(pkt))

# task 5
while True:
    # this will block until at least one interface is ready
    ready, _, _ = select.select([sock, tun], [], [])
    
    for fd in ready:
        if fd is sock:
            data, (ip, port) = sock.recvfrom(2048)
            pkt = IP(data)
            print("From socket <==: {} --> {}".format(pkt.src, pkt.dst))

            # Write the packet to the TUN interface.
            os.write(tun,bytes(pkt))

        if fd is tun:
            packet = os.read(tun, 2048)
            pkt = IP(packet)
            print("From tun    ==>: {} --> {}".format(pkt.src, pkt.dst))
            
            # Send the packet via the tunnel
            sock.sendto(packet, ("10.9.0.5",1234)) #port