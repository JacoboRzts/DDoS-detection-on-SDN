import json
from os import listdir
import argparse
import requests

parser = argparse.ArgumentParser(description="Script para cargar automaticamente los archivos de configuracion a OpenDayLight")
parser.add_argument("--ip", "-i", default="172.17.0.3", help="Direccion IPv4 del controlador ODL")
parser.add_argument("--path", "-p", default="instructions", help="Directorio con los JSON")
parser.add_argument("--flows", "-f", default=2, help="Numero de flows por checar")
args = parser.parse_args()

print('Saving the response: ')

for i in range(1, int(args.flows) + 1):
    url = f"http://{args.ip}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{i}/flow-node-inventory:table=0"
    r = requests.request(method='GET', url=url, auth=("admin", "admin"))
    if r.status_code == 200:
        json_data = r.json()
        name = f'{args.path}/flow_{i}.json'
        with open(name, 'w', encoding='utf-8') as new_file:
            json.dump(json_data, new_file, indent=2, ensure_ascii=False)
        print(f'Response saved as: {name}')
    
