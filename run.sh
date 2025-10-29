#!/bin/bash

TIME=$1    # Time to test        (20s by default)
HOST=$2    # Number of hosts     (3 by default)
SWITCH=$3  # Number of switch    (One by default)

echo "Starting the containers"
docker start controller mininet

echo "Uploading the network"
docker cp networks.py mininet:/root/

echo "Uploading the simulations"
docker cp simulate.py mininet:/root/

echo "Uploading the flows"
python3 -c "from generate_flows import tree_flows; tree_flows($HOST, $SWITCH)"
