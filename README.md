# DDoS detection on a SDN with Mininet and OpenDayLight 
DDoS detection on SDN is a project for the subjects: **Network Modeling and Simulation** and **Machine Learning** from the **UASLP**. The goal of this project is to create an intelligent system to detect and mitigate DDoS attacks on a SDN simulated using Mininet, as controller this project use OpenDayLight with the OpenFlow plugin to controll the flows in the network.


## Setup
How to set up and test:
1. Clone this repository using:
```sh
git clone https://github.com/JacoboRzts/DDoS-detection-on-SDN.git
```
2. Then run the deploy scripts to build and create the docker containers necessaries using:
```sh
sudo sh deploy
```
3. For the very first time you have to install the next tools in the mininet container:
```sh
apt update
apt install -y hping3 tshark netcat python3-numpy
```

4. Also need to install the OpenFlow plugin on the Opendaylight controller container:
```
feature:install odl-openflowplugin-flow-services-rest odl-openflowplugin-app-table-miss-enforcer odl-openflowplugin-nxm-extensions
```

5. After this you have to start the controller and mininet containers (you need to start always the controller first and don't have any other container running), in case you have some problems you need to check that the IP's for the controller in the "flows" and "networks" files are correct:
```sh
docker start controller mininet
```
6. To run a test you can execute the command:
```sh
sh simulate ping 3 2
```

The type of tests that you can run at the moment are:
- `normal`: execute a test with n switches and k hosts where each host run a ping with a random time and data size.
- `ping`: create the network with n switch and k hosts, and execute a `pingall`, then enter to the mininet CLI.
- `ddos`: execute a network with n switches and k host that start and DoS attack. 
- `spineleaf`: execute an experiment with 2 switches and 4 hosts with an especific flow (n and k params. are not necessaries).

Syntaxis:
```sh
sh simulate {normal | ping | ddos | spineleaf} [n] [k]
```

> Be careful with large number of hosts, especially with the DDoS simulation.

## TODO
There are a lot of things that could be good to implement or improve in this project, there is a list of some of they: 

Optimize:
- [ ] How the flows are removed.
- [ ] How the Spine Leaf instructions are loaded.

Problems: 
- [ ] The maximum size of a network is 6x5 hosts and one server.

Improvements: 
- [ ] Add a Dockerfile and docker-compose to the mininet network.
