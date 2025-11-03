import flows

def second_experiment_flows():
    print('Removing old flows')
    flows.cleanAll()
    print('Upload new flows')

    # Protocolos ARP
    for i in range(2, 5):
        flows.load(flows.define(id=f'{i}0', priority=4, eth_type=2054, out_port='NORMAL'), i)

    flows.load(flows.define(id=11, priority=1000, eth_type=2048, in_port='1', out_port=2), 1)
    flows.load(flows.define(id=12, priority=1000, eth_type=2048, in_port='2', out_port=1), 1)

    flows.load(flows.define(id=21, priority=1000, eth_type=2048, in_port='1', out_port=2), 2)
    flows.load(flows.define(id=22, priority=1000, eth_type=2048, in_port='2', out_port=1), 2)

    flows.load(flows.define(id=31, priority=8, eth_type=2048, ip_src='10.0.0.1/32', out_port=1), 3)
    flows.load(flows.define(id=32, priority=8, eth_type=2048, ip_src='10.0.0.2/32', out_port=2), 3)
    flows.load(flows.define(id=33, priority=9, eth_type=2048, ip_dst='10.0.0.1/32', out_port=3), 3)
    flows.load(flows.define(id=34, priority=9, eth_type=2048, ip_dst='10.0.0.2/32', out_port=4), 3)

    flows.load(flows.define(id=41, priority=8, eth_type=2048, ip_src='10.0.0.3/32', out_port=1), 4)
    flows.load(flows.define(id=42, priority=8, eth_type=2048, ip_src='10.0.0.4/32', out_port=2), 4)
    flows.load(flows.define(id=43, priority=9, eth_type=2048, ip_dst='10.0.0.3/32', out_port=3), 4)
    flows.load(flows.define(id=44, priority=9, eth_type=2048, ip_dst='10.0.0.4/32', out_port=4), 4)

def tree_flows(n_switch=1, n_host=2):
    flows.cleanAll()
    print('Upload new flows')
    for i in range(1, n_switch+3):
        flows.load(flows.define(id=f'{i}0', priority=4, eth_type=2054, out_port='NORMAL'), i)    # ARP
        flows.load(flows.define(id=f'{i}1', priority=9, eth_type=2048, out_port='NORMAL'), i)    # Normal IPv4 Flow
        if i > 1:
            flows.load(flows.define(id=f'{i}2', priority=1, eth_type=2048, ip_dst='10.0.0.0/16', out_port='1'), i)    # Flow to the main network
            flows.load(flows.define(id=f'1{i}', priority=1, eth_type=2048, ip_dst=f'10.0.{i-1}.0/16', out_port=f'{n_host+1}'), 1)    # Flow from the main network
