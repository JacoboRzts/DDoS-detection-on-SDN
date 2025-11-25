from mininet.log import setLogLevel
from mininet.cli import CLI
from random import randint
import networks
import sys

def spineleaf():
    """
    Start the Spine Leaf Topology on mininet.
    """
    net = networks.spineLeafNet()
    CLI(net)
    net.stop()

def ddos(n_switch=2, k_hosts=2):
    """
    Simulate a DDoS attack with NxK switches and hosts, with the tree topology.
    """
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('server')

    # Start the simple web server
    print(f'>>> Starting the simple web server on server')
    victim.cmd('python3 -m http.server 80 &')

    mon_size = 0.4
    monitors, attackers = networks.splitHosts(net.hosts[1:], mon_size)

    print(f'>>> DoS attack start with {(1 - mon_size) * 100}% of attackers')

    print('>>> Attackers: ', end='')
    for attacker in attackers:
        size = randint(64, 1024)
        attacker.cmd(f'hping3 -S -p 80 --rand-source --flood -d {size} 10.0.0.1 &')
        attacker.cmd(f'echo "{size}" >> datasets/size_ddos.csv')
        print(attacker.name, end=' ')
    print()

    print('>>> Monitors: ', end='')
    for monitor in monitors:
        print(monitor.name, end=' ')
    print()

    print('\n>>> Starting CLI')
    CLI(net)
    net.stop()

def normal(n_switch=2, n_host=3):
    """
    Simulate a normal traffic of a network using the tree topology.
    """
    net = networks.tree(n_switch, n_host)
    hosts = net.hosts[1:]
    victim = net.hosts[0]

    print(f'>>> Starting the simple web server on server')
    victim.cmd('python3 -m http.server 80 &')

    print('>>> Simulating the network traffic')
    for host in hosts:
        size = randint(8, 1024)
        host.cmd(f'hping3 -S --rand-source -d {size} -p 80 --fast 10.0.0.1 &')
        host.cmd(f'echo "{size}" >> datasets/size_normal.csv')
    CLI(net)
    net.stop()

def conectivity(n_switch=2, n_host=3):
    """
    Start a tree topology and inmediatly run a ping test.
    """
    net = networks.tree(n_switch, n_host)
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        type = (sys.argv[1])

    setLogLevel('output')
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
