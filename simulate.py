from mininet.log import setLogLevel
from mininet.cli import CLI
import networks
import sys

def ddos(n_switch=2, k_hosts=2, seconds=10):
    setLogLevel('info')
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('h01')

    # Start the simple web server
    victim.cmd(f'python3 -m http.server &')

    for i in range(1, n_switch):
        for j in range(1, k_hosts + 1):
            host = net.get(f'h{i}{j}')
            host.cmd(f'hping3 -S --rand-source --flood -d 2048 {victim.IP()} &')

    CLI(net)
    net.stop()

def normal(n_switch=2, n_host=3):
    setLogLevel('output')
    print('Starting the netowork ')
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
                if len(sys.argv) > 4:
                    time = int(sys.argv[4])
                    ddos(switchs, hosts, time)
                else:
                    print('Para el test DDoS se necesita el parametro tiempo al final')
            case _:
                print('No se selecciono ningun tipo de test')
    else:
        print('Se necesita al menos un argumento.')
