#!/usr/bin/env python3

from mininet.cli import CLI
from mininet.log import setLogLevel
import networks

def test():
    net = networks.tree(n_switch=2, n_host=3)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test()
