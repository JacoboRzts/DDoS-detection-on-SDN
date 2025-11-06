#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController, CPULimitedHost
from mininet.link import TCLink

CONTROLLER_IP = "172.17.0.2"
CONTROLLER_PORT = 6653

def simple(n=3):
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink, host=CPULimitedHost)
    net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT )
    switch = net.addSwitch('s1', protocols="OpenFlow13")
    for i in range(n):
        host = net.addHost(f'h{i+1}')
        net.addLink(switch, host)

    net.build()
    net.start()
    return net

def tree(n_switch=1, n_host=2):
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    c1 = net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    switch_array = []
    switch_array.append(net.addSwitch(name='s1', protocols="OpenFlow13"))
    net.addLink(switch_array[0], net.addHost(f'server', ip=f'10.0.0.1/16', cpu=0.01), bw=4)

    for i in range(1, n_switch+1):
        switch_array.append(net.addSwitch(f's{i+1}', protocols="OpenFlow13"))
        net.addLink(switch_array[i], switch_array[0])
        for j in range(n_host):
            net.addLink(switch_array[i], net.addHost(f'h{i}{j+1}', ip=f'10.0.{i}.{j+1}/16'))

    switch_array.append(net.addSwitch(name=f's{n_switch+2}', protocols="OpenFlow13"))
    net.addLink(switch_array[-1], switch_array[0])
    net.addLink(switch_array[-1], net.addHost('monitor', ip=f'10.0.{n_switch+1}.1/16'))

    net.build()
    c1.start()
    for switch in switch_array:
        switch.start([c1])
    net.start()

    return net
