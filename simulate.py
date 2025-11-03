from mininet.log import setLogLevel
from mininet.cli import CLI
import networks
import sys

def ddos(n_switch=2, k_hosts=2, seconds=10):
    setLogLevel('output')
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('server')

    # Start the simple web server
    print(f'Starting web server from server with IP {victim.IP()}')
    victim.cmd(f'python3 -m http.server 80 &')

    hosts = net.hosts
    for host in hosts[1:-1]:
        print(f'Starting DoS attack from {host.name} to {victim.IP()}')
        # SYN
        host.cmd(f'hping3 -S --rand-source --flood -d 2048 {victim.IP()} &')
        # ICMP
        # host.cmd(f'hping3 -1 --rand-source --flood -d 4000 {victim.IP()} &')

    CLI(net)
    net.stop()

def normal(n_switch=2, n_host=3):
    setLogLevel('output')
    net = networks.tree(n_switch, n_host)
    CLI(net)
    net.stop()

def conectivity(n_switch=2, n_host=3):
    setLogLevel('info')
    net = networks.tree(n_switch, n_host)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    if len(sys.argv) > 3:

        type = sys.argv[1]
        switchs = int(sys.argv[2])
        hosts = int(sys.argv[3])

        match type:
            case 'normal':
                normal(switchs, hosts)
            case 'ddos':
                ddos(switchs, hosts)
            case _:
                print('No se selecciono ningun tipo de test')
    else:
        print('Se necesita al menos un argumento.')
