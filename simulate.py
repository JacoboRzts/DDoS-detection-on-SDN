from mininet.log import setLogLevel
from mininet.cli import CLI
import networks
import sys

def ddos(n_switch=2, k_hosts=2, seconds=10):
    setLogLevel('info')
    net = networks.tree(n_switch, k_hosts)

    victim = net.get('h01')
    listener = net.get('h02')

    switch = net.get('s1')
    hosts = []

    for i in range(2, n_switch+1):
        for j in range(1, k_hosts+1):
            hosts.append(net.get(f'h{i-1}{j}'))

    victim.cmd(f'timeout {seconds + 1} python3 -m http.server &')

    # Start the traffic snif
    switch.cmd(f'timeout {seconds + 1} tshark -i s1-eth1 -f "dst host {victim.IP()} and not arp" -w ddos.pcap')

    # Start the attack from N hosts
    for host in hosts:
        host.cmd(f'timeout {seconds} hping3 -S -p 80 --rand-source -d 1000 --faster {victim.IP()} &')

    listener.cmd(f'timeout {seconds} ping {victim.IP()} >> check.out')


    net.stop()

def normal(n_switch=2, n_host=3):
    setLogLevel('info')
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
