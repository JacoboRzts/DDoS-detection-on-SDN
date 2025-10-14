#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink

import networks
import time

def test(n_hosts=3, seconds=10):
    net = networks.simple(n_hosts)
    
    server  = net.get('server')
    listener = net.get('L')
    s0 = net.get('s0')
    
    hosts = []

    for i in range(n_hosts):
        hosts.append(net.get(f'h{i + 1}') )

    file = f'ddos_snif.pcap'

    print(f'Starting the test with {n_hosts}')
    
    # Start the traffic snif
    s0.cmd(f'timeout {seconds + 1} tshark -i s0-eth1 -f "dst host {server.IP()} and not arp" -w {file}')
    
    # Start the attack from N hosts
    for host in hosts:
        host.cmd(f'timeout {seconds} hping3 -S -p 80 --rand-source -d 1000 --faster {server.IP()} &')
    
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test()

