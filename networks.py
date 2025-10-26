#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink

CONTROLLER_IP = "172.17.0.2"
CONTROLLER_PORT = 6653

def simple(n=3):
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT )
    switch = net.addSwitch('s1', protocols="OpenFlow13")
    for i in range(n):
        host = net.addHost(f'h{i+1}')
        net.addLink(switch, host)

    net.build()
    net.start()
    return net

def tree(n_switch=1, n_host=2):
    net = Mininet(controller=RemoteController, switch=OVSSwitch)
    c1 = net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    switch_array = []

    for i in range(n_switch):
        switch_array.append(net.addSwitch(f's{i+1}', protocols="OpenFlow13"))
        if i > 0:
            net.addLink(switch_array[i], switch_array[0])
        for j in range(n_host):
            net.addLink(switch_array[i], net.addHost(f'h{i}{j+1}', ip=f'10.0.{i}.{j+1}/24'))

    net.build()
    c1.start()
    for switch in switch_array:
        switch.start([c1])
    net.start()

    return net
