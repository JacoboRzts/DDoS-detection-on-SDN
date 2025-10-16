#!/usr/bin/env python3

from mininet.cli import CLI
from mininet.log import setLogLevel
import networks

def test():
    net = networks.tree()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    test()
