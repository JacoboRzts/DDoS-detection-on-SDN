#!/bin/bash

$PATH = $1    # Path of the files
$TIME = $2    # Time to test        (20s by default)
$HOST = $3    # Number of hosts     (3 by default)
$SWITCH = $4  # Number of switch    (One by default)

# Copy the network to mininet
docker cp $PATH/ddos.py mininet:/root/

# Remove the old flows from the controller
python3 del_flows.py

# Generates and load the new flows to the controller
python3 gen_flows.py $HOST $SWITCH

# Run the test
docker exec mininet $PATH/ddos.py $TIME $HOST 

# Wait to the test to finish
sleep $TIME + 1

# Copy the results 
docker cp mininet:/root/snif/ddos_snif.pcap $PATH/traffic/
