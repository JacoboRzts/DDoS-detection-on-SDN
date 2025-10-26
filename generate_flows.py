import requests
import json

CONTROLLER_IP='172.17.0.2'
AUTH=('admin', 'admin')

# Creates a flow with the given values
# id: the id of the flow
# eth_type: the ethernet type, 2048 for IPv4 and 2054 for ARP protocol
# ip_dst: the IPv4 destination in a string, for example: '0.0.0.0/32' if it is setted to 0 then the field its not setted.
# out_node: the output node it could be a number or a string like: 'NORMAL'
def define_flow(id, priority, eth_type, out_port, in_port='', ip_src='', ip_dst='', switch=1):
    flow = {
        "flow": [
            {
                "table_id": 0,
                "id": id,
                "priority": priority,
                "cookie": priority,
                "match": {
                    "ethernet-match": {
                        "ethernet-type": {
                            "type": eth_type
                        }
                    }
                },
                "instructions": {
                    "instruction": [
                        {
                            "order": 0,
                            "apply-actions": {
                                "action": [
                                    {
                                        "order": 0,
                                        "output-action": {
                                            "output-node-connector": out_port
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }
    if ip_src != '':
        flow['flow'][0]['match']['ipv4-source'] = ip_src
    if ip_dst !='':
        flow['flow'][0]['match']['ipv4-destination'] = ip_dst
    if in_port != '':
        flow['flow'][0]['match']['in-port'] = f'openflow:{switch}:{in_port}'
    return flow

def load_flow(flow, id):
    id_flow = flow['flow'][0]['id']
    url = f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{id}/flow-node-inventory:table=0/flow={id_flow}'
    req = requests.request(method='PUT', json=flow, url=url, auth=('admin', 'admin'), headers={'Content-Type': 'application/json'})
    print(f'{id_flow}: {req.status_code}')
    # print(json.dumps(flow, indent=2))

def clean_flows():
    for i in range(1, 10):
        req = requests.get(auth=AUTH, url=f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{i}/flow-node-inventory:table=0')
        if req.status_code // 100 == 2:
            flows = req.json()['flow-node-inventory:table'][0]
            if 'flow' in flows:
                for flow in flows['flow']:
                    rd = requests.delete(auth=AUTH, url=f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{i}/flow-node-inventory:table=0/flow={flow["id"]}')
                    print(flow['id'], rd.status_code)

def simple_test(n_switch=1, n_host=2):
    for i in range(1, n_switch+1):
        load_flow(define_flow(id=f'{i}0', priority=4, eth_type=2054, out_port='NORMAL'), i)    # ARP
        load_flow(define_flow(id=f'{i}1', priority=9, eth_type=2048, out_port='NORMAL'), i)    # Normal IPv4 Flow
        if i > 1:
            load_flow(define_flow(id=f'{i}2', priority=1, eth_type=2048, ip_dst='10.0.0.0/24', out_port='1'), i)    # Flow to the main network
            load_flow(define_flow(id=f'1{i}', priority=1, eth_type=2048, ip_dst=f'10.0.{i-1}.0/24', out_port=f'{n_host+1}'), 1)    # Flow from the main network


def test_second_experiment():
    # Protocolos ARP
    for i in range(2, 5):
        load_flow(define_flow(id=f'{i}0', priority=4, eth_type=2054, out_port='NORMAL'), i)

    load_flow(define_flow(id=11, priority=1000, eth_type=2048, in_port='1', out_port=2), 1)
    load_flow(define_flow(id=12, priority=1000, eth_type=2048, in_port='2', out_port=1), 1)

    load_flow(define_flow(id=21, priority=1000, eth_type=2048, in_port='1', out_port=2), 2)
    load_flow(define_flow(id=22, priority=1000, eth_type=2048, in_port='2', out_port=1), 2)

    load_flow(define_flow(id=31, priority=8, eth_type=2048, ip_src='10.0.0.1/32', out_port=1), 3)
    load_flow(define_flow(id=32, priority=8, eth_type=2048, ip_src='10.0.0.2/32', out_port=2), 3)
    load_flow(define_flow(id=33, priority=9, eth_type=2048, ip_dst='10.0.0.1/32', out_port=3), 3)
    load_flow(define_flow(id=34, priority=9, eth_type=2048, ip_dst='10.0.0.2/32', out_port=4), 3)

    load_flow(define_flow(id=41, priority=8, eth_type=2048, ip_src='10.0.0.3/32', out_port=1), 4)
    load_flow(define_flow(id=42, priority=8, eth_type=2048, ip_src='10.0.0.4/32', out_port=2), 4)
    load_flow(define_flow(id=43, priority=9, eth_type=2048, ip_dst='10.0.0.3/32', out_port=3), 4)
    load_flow(define_flow(id=44, priority=9, eth_type=2048, ip_dst='10.0.0.4/32', out_port=4), 4)

print('Removing old flows')
clean_flows()
print('Upload new flows')
simple_test(n_switch=2, n_host=3)
