# robocom-benchmarks

The purpose of this repo is to create a semi-automated setup to benchmark different implementations of middlewares for robotic communications.
The main use case that drove the development of this benchmark is minimizing total bandwidth usage for systems that need to report their status regularly, for example for robots that need to send a heartbeat status over a metered network (i.e. a SIM card).

## Requirements

The setup is based on mininet, you will need:

* A Linux distro, tested on Ubuntu 20.04
* [Mininet](http://mininet.org/), deb version works fine.
* [Cyclonedds](https://github.com/eclipse-cyclonedds/cyclonedds), built from source
* [Zenoh](https://zenoh.io/), deb version works fine.
* venv was used to install cyclone and dependencies locally.
* [Mosquitto MQTT](https://mosquitto.org/) version 2.0.10 installed via [PPA](https://launchpad.net/~mosquitto-dev/+archive/ubuntu/mosquitto-ppa)
