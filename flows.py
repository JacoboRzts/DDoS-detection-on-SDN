import requests
import json

CONTROLLER_IP='172.17.0.2'
AUTH=('admin', 'admin')

"""
Creates a flow with the given values
id: the id of the flow
eth_type: the ethernet type, 2048 for IPv4 and 2054 for ARP protocol
ip_dst: the IPv4 destination in a string, for example: '0.0.0.0/32' if it is setted to 0 then the field its not setted.
out_node: the output node it could be a number or a string like: 'NORMAL'
"""
def define(id, priority, eth_type, out_port, in_port='', ip_src='', ip_dst='', switch=1):
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

def load(flow, id):
    id_flow = flow['flow'][0]['id']
    url = f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{id}/flow-node-inventory:table=0/flow={id_flow}'
    req = requests.request(method='PUT', json=flow, url=url, auth=('admin', 'admin'), headers={'Content-Type': 'application/json'})
    print(f'{id_flow}: {req.status_code}')
    # print(json.dumps(flow, indent=2))

def cleanAll():
    for i in range(1, 10):
        req = requests.get(auth=AUTH, url=f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{i}/flow-node-inventory:table=0')
        if req.status_code // 100 == 2:
            flows = req.json()['flow-node-inventory:table'][0]
            if 'flow' in flows:
                for flow in flows['flow']:
                    rd = requests.delete(auth=AUTH, url=f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{i}/flow-node-inventory:table=0/flow={flow["id"]}')
                    print(flow['id'], rd.status_code)
