#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink
from time import time_ns

C_IP = "172.17.0.3"
C_PORT = 6653

def network(n):
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    c1 = net.addController("c1", controller=RemoteController, ip=C_IP, port=C_PORT)
    s1 = net.addSwitch('s1', protocols="OpenFlow13")
    s2 = net.addSwitch('s1', protocols="OpenFlow13")
    
    for i in range(N):
        host = net.addHost(f'h{i + 1}')
        net.addLink(s1, host)

    server = net.addHost('server')
    net.addLink(s2, net.addHost('l1'))
    net.addLink(s2, net.addHost('l2'))
    net.addLink(s2, server, bw=5, max_quere_size=100)

    net.build()
    c1.start()
    net.start()
    return net

def test(n):
    net = network()

    attacker = net.get('h1')
    victim = net.get('h2')
    listener = net.get('h3')
    switch = net.get('s1')

    file = f'test_1_{switch.name}.pcap'

    print('Iniciando el test')
    
    # Inicia la escucha
    switch.cmd(f'tshark -i s1-eth2 -f "host {victim.name}" -w {file}')

    # Inicia el reloj...
    start_time = time_ns()
    
    # Inicia el ataque
    attacker.cmd(f'hping3 -S -p 80 --rand-source -d 1000 --faster {victim.IP()}')

    # Espera a que el servidor se sature
    while True:
        response = listener.cmd(f'wget -q -O- --server-response {victim.IP()} 2>&1 | head -n 1')
        if "200" in response:
            break
        else: 
            sleep(1)

    total_time = start_time - time_ns()
    
    switch.cmd('pkill tshark')
    attacker.cmd('pkill hping3')

    print(f'Test finalizado\nEl servidor cayo en: {total_time}ns\nCaptura guardada en: {file}')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test()

