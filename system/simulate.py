from mininet.log import setLogLevel
from mininet.cli import CLI
import networks
import sys
import numpy as np
from random import randint
from math import floor

def splitHosts(hosts, monitor_size):
    """
    Separate an array of mininet host into two parts.
    hosts: array with mininet hosts
    monitor_size: % of the number of monitors in the network, as a float for example: 0.4 -> 40% monitors and 60% attackers
    """
    size = floor(monitor_size * len(hosts))
    np.random.shuffle(hosts)
    monitors = hosts[:size-1]
    attackers = hosts[size:]
    return monitors, attackers

def spineleaf():
    """
    Start the Spine Leaf Topology on mininet.
    """
    setLogLevel('output')
    net = networks.spineLeafNet()
    CLI(net)
    net.stop()

def ddos(n_switch=2, k_hosts=2):
    """
    Simulate a DDoS attack with NxK switches and hosts, with the tree topology.
    """
    setLogLevel('output')
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('server')

    # Start the simple web server
    print(f'>>> Starting the simple web server on server')
    victim.cmd('python3 -m http.server 80 &')

    monitors, attackers = splitHosts(net.hosts[1:], 0.4)

    print('>>> DoS attack start')

    print('>>> Attackers: ', end='')
    for attacker in attackers:
        size = randint(64, 1024)
        attacker.cmd(f'hping3 -S -p 80 --rand-source --flood -d {size} 10.0.0.1 &')
        print(attacker.name, end=' ')
    print()

    print('>>> Monitors: ', end='')
    for monitor in monitors:
        print(monitor.name, end=' ')
    print()

    CLI(net)
    net.stop()

def normal(n_switch=2, n_host=3):
    """
    Simulate a normal traffic of a network using the tree topology.
    """
    setLogLevel('output')
    net = networks.tree(n_switch, n_host)
    hosts = net.hosts[1:]
    victim = net.hosts[0]

    print(f'>>> Starting the simple web server on server')
    victim.cmd('python3 -m http.server 80 &')

    print('>>> Simulating the network traffic')
    for host in hosts:
        size = randint(8, 1024)
        host.cmd(f'hping3 -S --rand-source -d {size} -p 80 --fast 10.0.0.1 &')
    CLI(net)
    net.stop()

def conectivity(n_switch=2, n_host=3):
    """
    Start a tree topology and inmediatly run a ping test.
    """
    setLogLevel('output')
    net = networks.tree(n_switch, n_host)
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = (sys.argv[1])

    if len(sys.argv) > 3 :
        type = (sys.argv[1])
        switchs = int(sys.argv[2])
        hosts = int(sys.argv[3])

        match type:
            case 'ping':
                conectivity(switchs, hosts)
            case 'normal':
                normal(switchs, hosts)
            case 'ddos':
                ddos(switchs, hosts)
            case _:
                print('No se selecciono ningun tipo de test')
    else:
        if type == 'spineleaf':
            spineleaf()
        else:
            print('Se necesita al menos un argumento.')
