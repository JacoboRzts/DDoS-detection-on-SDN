import requests

#   Creates a flow with the given values
#   id: the id of the flow
#   eth_type: the ethernet type, 2048 for IPv4 and 2054 for ARP protocol
#   ip_dst: the IPv4 destination in a string, for example: '0.0.0.0/32' if it is setted to 0 then the field its not setted.
#   out_node: the output node it could be a number or a string like: 'NORMAL'
def flow(id, priority, eth_type, out_port, in_port=False, ip_src=False, ip_dst=False):
    flow = {
        "flow": [
            {
                "table_id": 0,
                "id": id,
                "priority": priority,
                "cookie": "9",
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
    if ip_src:
        flow['flow'][0]['match']['ipv4-source'] = ip_src
    if ip_dst:
        flow['flow'][0]['match']['ipv4-destination'] = ip_dst
    if in_port:
        flow['flow'][0]['match']['in-port'] = f'openflow:{id // 10}:{in_port}'
    return flow

def load_flow(flow, c_ip='172.17.0.2'):
    id_flow = flow['flow'][0]['id']
    endpoint = f'http://{c_ip}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{int(id_flow) // 10}/flow-node-inventory:table=0/flow={id_flow}'
    r = requests.request(method='PUT', json=flow, url=endpoint, auth=('admin', 'admin'), headers={'Content-Type': 'application/json'})
    print(r.status_code)

def upload_all(n_switch=1, n_host=3):
    load_flow(flow(id='10', priority=9, eth_type=2054, out_port='NORMAL'))      # Flow for the ARP protocol in s0
    load_flow(flow(id='11', priority=5, eth_type=2048, ip_dst='10.0.0.1/32', out_port=1))   # Flow from s0 to the server
    load_flow(flow(id='12', priority=5, eth_type=2048, ip_dst='10.0.0.2/32', out_port=2))   # Flow from s0 to L
    load_flow(flow(id='13', priority=3, eth_type=2048, ip_dst='10.0.0.0/16', out_port=3))   # Flow for the 'internet'

    for i in range(1, n_switch + 1):
        print(f'Loading flows for the switch {i}')
        load_flow(flow(id=f'{i+1}0', priority=5, eth_type=2048, ip_dst='10.0.0.0/24', out_port=1))
        for j in range(1, n_host + 1):
            print(f'host {i}{j}', end=' ')
            load_flow(flow(id=f'{i+1}{j}', priority=5, eth_type=2048, ip_dst=f'10.0.{i}.{j}/32', out_port=j+1))

upload_all()
