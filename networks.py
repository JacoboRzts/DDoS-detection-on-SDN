#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink

CONTROLLER_IP = "172.17.0.2"
CONTROLLER_PORT = 6653

def simple(n=2):
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT )
    switch = net.addSwitch('s1', protocols="OpenFlow13")
    for i in range(n):
        host = net.addHost(f'h{i+1}')
        net.addLink(switch, host)

    net.build()
    net.start()
    return net


def tree(n_switch=1, n_host=3):
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT )
    s0 = net.addSwitch('s0', protocols="OpenFlow13")

    for i in range(1, n_switch + 1):
        switch = net.addSwitch(f's{i}', protocols="OpenFlow13")
        net.addLink(switch, s0)
        for j in range(1, n_host + 1):
            host = net.addHost(f'h{i}{j}', ip=f'10.0.0.{i}{j}/24')
            net.addLink(switch, host)

    server = net.addHost('srv')
    listener = net.addHost('lst')
    net.addLink(s0, server)
    net.addLink(s0, listener)

    net.build()
    net.start()
    return net
