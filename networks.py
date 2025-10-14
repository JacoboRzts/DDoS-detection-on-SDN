#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.log import setLogLevel
from mininet.link import TCLink
from time import time_ns

CONTROLLER_IP = "172.17.0.3"
CONTROLLER_PORT = 6653

def base():
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    c1 = net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT )
    s0 = net.addSwitch('s0', protocols="OpenFlow13")
    server = net.addHost('server')
    listener = net.addHost('L')
    net.addLink(s0, server)
    net.addLink(s0, listener)
    return net


def simple(n_hosts=3):
    net = base()
    s1 = net.addSwitch('s1', protocols='OpenFlow13')

    for i in range(n_hosts):
        host = net.addHost(f'h{i + 1}')
        net.addLink(s1, host)
    
    net.build()
    net.start()
    return net


def complete(n_switch=3, n_hosts=3):
    net = base()

    for i in range(n_switch):
        switch = net.addSwitch(f's{i + 1}', protocols="OpenFlow13")
        for j in range(n_hosts):
            host = net.addHost(f'h{i+1}_{j+1}')
            net.addLink(switch, host)

    net.build()
    net.start()
    return net


