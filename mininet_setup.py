import argparse
import time
import numpy as np

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import dumpNodeConnections

class Network:

    def __init__(self):
        self.machines = ['0_router', '1_sub', '2_pub']
        self.bringup()

    def bringup(self):
        topo = Topo()
        switch = topo.addSwitch('s1')

        for i in range(0, len(self.machines)):
            host = topo.addHost(f'{self.machines[i]}')
            print(host)
            topo.addLink(host, switch)

        self.net = Mininet(topo)

        # Disable ipv6
        for switch in self.net.switches:
            switch.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
            switch.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
            switch.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")

        for host in self.net.hosts:
            host.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
            host.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
            host.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
            iface = f'{host.name}-eth0'
            host.cmd(f'route add -net 224.0.0.0 netmask 224.0.0.0 {iface}')

        self.net.start()
        #self.net.pingAll()

    def waitCompletion(self, ifconfig_report=True, debug_output=False):
        for i, host in enumerate(self.net.hosts):
            while host.waiting:
                text = host.monitor(1000)
                if debug_output:
                    print(text)

        for host in self.net.hosts:
            host.sendCmd('ifconfig')

        for i, host in enumerate(self.net.hosts):
            while host.waiting:
                text = host.monitor(1000)
                if ifconfig_report:
                    print(text)


    def testZenoh(self):
        input("Press enter to start zenoh test")
        # Run the router
        router = self.net.hosts[0]
        router.cmd('zenohd &')
        time.sleep(1)
        # Now setup the publisher and subscriber
        # For now only one each
        sub = self.net.hosts[1]
        pub = self.net.hosts[2]
        print("Running subscriber")
        sub.sendCmd('python3 zenoh/zenoh_processes.py -d 21 --role sub')
        time.sleep(0.5)
        print("Running publisher")
        pub.sendCmd('python3 zenoh/zenoh_processes.py -d 20 --role pub')

        self.waitCompletion()

        # Kill the router
        print("Killing router")
        router.cmd('killall -9 zenohd')
        self.teardown()


    def testCyclone(self, static_discovery=False):
        input("Press enter to start cyclone test")

        # Cyclone doesn't use a router, skip it
        sub = self.net.hosts[1]
        pub = self.net.hosts[2]

        print("Running subscriber")
        sub.sendCmd('cyclone/build/HelloworldSubscriber 21')
        time.sleep(0.5)
        print("Running publisher")
        pub.sendCmd('cyclone/build/HelloworldPublisher 20')

        self.waitCompletion()
        self.teardown()

    def teardown(self):
        self.net.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',
            dest='middleware',
            type=str,
            required=True,
            help='Middleware to test',
            choices = ['cdds', 'zenoh'])

    parser.add_argument('--static',
            dest='static',
            type=bool,
            default=False,
            help='Whether to perform static discovery for DDS')

    args = parser.parse_args()
    net = Network()
    if args.middleware == 'cdds':
        net.testCyclone(args.static)
    if args.middleware == 'zenoh':
        # No static configuration for Zenoh
        net.testZenoh()
