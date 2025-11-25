#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController, CPULimitedHost
from mininet.link import TCLink
from math import floor
from numpy.random import shuffle

CONTROLLER_IP = "172.17.0.2"
CONTROLLER_PORT = 6653

def tree(n_switch=1, n_host=2):
    """
    Define a mininet network with the simple tree topology, where each switch has k host and is connected with the s1 first switch that only has a server host.
    """
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    c1 = net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    switch_array = []
    switch_array.append(net.addSwitch(name='s1', protocols="OpenFlow13"))
    net.addLink(switch_array[0], net.addHost(name=f'server', ip=f'10.0.0.1/16', mac='AA:'*6), bw=4)

    for i in range(1, n_switch+1):
        switch_array.append(net.addSwitch(f's{i+1}', protocols="OpenFlow13"))
        net.addLink(switch_array[i], switch_array[0])
        for j in range(n_host):
            net.addLink(switch_array[i], net.addHost(f'h{i}{j+1}', ip=f'10.0.{i}.{j+1}/16', mac='00:'*5+f'{i}{j}' ))

    net.build()
    c1.start()
    for switch in switch_array:
        switch.start([c1])
    net.start()

    net.waitConnected()

    return net

def spineLeafNet(n=4):
    """
    Define a spine leaf topology on mininet and connect with the controller
    """
    if n < 4 or n % 2 == 1:
        return False

    net = Mininet(controller=RemoteController, switch=OVSSwitch)
    c1 = net.addController('c1', controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT)

    switchArray = []

    for i in range(n):
        switchArray.append(net.addSwitch(f"s{i + 1}", protocols="OpenFlow13"))

    hostArray = []
    for i in range(n):
        hostArray.append(net.addHost(f"h{i + 1}"))

    for i in range(n // 2):
        for j in range(n // 2, n):
            net.addLink(switchArray[i], switchArray[j])

    j = 0
    for i in range(n // 2, n):
        net.addLink(switchArray[i], hostArray[j])
        j += 1
        net.addLink(switchArray[i], hostArray[j])
        j += 1

    net.build()
    c1.start()
    for switch in switchArray:
        switch.start([c1])
    net.start()
    return net

def splitHosts(hosts, monitor_size):
    """
    Separate an array of mininet host into two parts.
    hosts: array with mininet hosts
    monitor_size: % of the number of monitors in the network, as a float for example: 0.4 -> 40% monitors and 60% attackers
    """
    size = floor(monitor_size * len(hosts))
    shuffle(hosts)
    monitors = hosts[:size-1]
    attackers = hosts[size:]
    return monitors, attackers
