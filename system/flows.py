import requests

CONTROLLER_IP='172.17.0.2'
AUTH=('admin', 'admin')

def define(id, priority, eth_type, out_port, in_port='', ip_src='', ip_dst='', switch=1):
    """
    Creates a json flow with the given values.
    id: identifier of the flow.
    priority: priority of the flow have to be and integer or a string with and integer.
    eth_type: ethernet type to the flow to match (hexadecimal code).
    out_port: output port of the flow, could be an interface or 'NORMAL'.
    in_port: input interface of the switch, positive integer.
    ip_src: IPv4 to match on input, if neccesary
    ip_dst: IPv4 to match on output, if neccesary
    """
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
    """
    Load a json flow generated on the IP openflow node.
    flow: previous defined json flow with the function define()
    id: the switch or openflow node number to where the flow is going to be updated.
    """
    id_flow = flow['flow'][0]['id']
    url = f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{id}/flow-node-inventory:table=0/flow={id_flow}'
    req = requests.request(method='PUT', json=flow, url=url, auth=('admin', 'admin'), headers={'Content-Type': 'application/json'})
    # print(f'{id_flow}: {req.status_code}')

def cleanAll():
    """
    Removes ALL the flows of the controller, to avoid collisions.
    """
    print('Removing old flows')
    for i in range(1, 10):
        req = requests.get(auth=AUTH, url=f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{i}/flow-node-inventory:table=0')
        if req.status_code // 100 == 2:
            flows = req.json()['flow-node-inventory:table'][0]
            if 'flow' in flows:
                for flow in flows['flow']:
                    rd = requests.delete(auth=AUTH, url=f'http://{CONTROLLER_IP}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{i}/flow-node-inventory:table=0/flow={flow["id"]}')
                    # print(flow['id'], rd.status_code)
