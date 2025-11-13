from mininet.log import setLogLevel
from mininet.cli import CLI
import networks
import sys
import numpy as np
from math import floor

def splitHosts(hosts, monitor_size):
    size = floor(monitor_size * len(hosts))
    print(f'size = {size}')
    np.random.shuffle(hosts)
    monitors = hosts[:size-1]
    attackers = hosts[size:]
    return monitors, attackers

def ddos(n_switch=2, k_hosts=2, type='icmp', time=20):
    setLogLevel('output')
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('server')

    # Start the simple web server
    print(f'Starting web server from server with IP {victim.IP()}:80')
    victim.cmd(f'python3 -m http.server 80 &')

    if type == 'syn':
        cmd_attack = f'hping3 -S --rand-source --flood -d 2048 -p 80 {victim.IP()} &'
    else:
        cmd_attack = f'hping3 -1 --rand-source --flood -d 1024 {victim.IP()} &'

    hosts = net.hosts
    monitors, attackers = splitHosts(net.hosts[1:], 0.5)

    for attacker in attackers:
        attacker.cmd(cmd_attack)
        print(f'{type.upper()} DoS attack started from {attacker.name}')

    CLI(net)
    net.stop()

def normal(n_switch=2, n_host=3):
    setLogLevel('output')
    net = networks.tree(n_switch, n_host)
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
                if len(sys.argv) > 4:
                    type = sys.argv[4]
                    ddos(switchs, hosts, type)
                else:
                    ddos(switchs, hosts)
            case _:
                print('No se selecciono ningun tipo de test')
    else:
        print('Se necesita al menos un argumento.')
