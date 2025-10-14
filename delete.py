import json
from os import listdir
import argparse
import requests

parser = argparse.ArgumentParser(description="Script para cargar automaticamente los archivos de configuracion a OpenDayLight")
parser.add_argument("--ip", "-i", default="172.17.0.3", help="Direccion IPv4 del controlador ODL")
parser.add_argument("--path", "-p", default="instructions", help="Directorio con los JSON")
args = parser.parse_args()

files = listdir(args.path + '/')

print('Deleting files: ')

for file in files:
    print(file, end=': ')
    with open(args.path + '/' + file, "r", encoding="utf-8") as file:
        data = json.load(file)
    id = int(data["flow"][0]["id"])
    src = f"http://{args.ip}:8181/rests/data/opendaylight-inventory:nodes/node=openflow:{id // 100}/flow-node-inventory:table=0/flow={id}"
    req = requests.request(method='DELETE', url=src, auth=("admin", "admin"))
    print(req.status_code)
    
    
