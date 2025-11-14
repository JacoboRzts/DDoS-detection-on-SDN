from mininet.log import setLogLevel
from mininet.cli import CLI
import networks
import sys
import numpy as np
from random import randint
from math import floor

def splitHosts(hosts, monitor_size):
    size = floor(monitor_size * len(hosts))
    np.random.shuffle(hosts)
    monitors = hosts[:size-1]
    attackers = hosts[size:]
    return monitors, attackers

def ddos(n_switch=2, k_hosts=2):
    setLogLevel('output')
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('server')

    # Start the simple web server
    print(f'Starting web server from server with IP {victim.IP()}:80')
    victim.cmd(f'python3 -m http.server 80 &')

    hosts = net.hosts
    monitors, attackers = splitHosts(net.hosts[1:], 0.4)

    for attacker in attackers:
        size = randint(64, 2048)
        attacker.cmd(f'hping3 -S --rand-source --flood -d {size} -p 80 {victim.IP()} &')
        print(f'DoS attack started from {attacker.name} with {size} data size.')

    # monitors[0].cmd(f'ping -c 50 -q {victim.IP()} >> test{n_switch}x{k_hosts}.txt')

    CLI(net)
    net.stop()

def normal(n_switch=2, n_host=3):
    setLogLevel('output')
    net = networks.tree(n_switch, n_host)
    hosts = net.hosts[1:]
    victim = net.hosts[0]
    for host in hosts:
        size = randint(32, 1024)
        time = randint(10000, 100000)
        print(f'Random message from {host.name} with size {size}')
        host.cmd(f'hping3 -S --rand-source -d {size} -p 80 -i u{time} {victim.IP()} &')
    CLI(net)
    net.stop()

def conectivity(n_switch=2, n_host=3):
    setLogLevel('output')
    net = networks.tree(n_switch, n_host)
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    if len(sys.argv) > 3:

        type = sys.argv[1]
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
        print('Se necesita al menos un argumento.')
