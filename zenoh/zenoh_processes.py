import argparse
import numpy as np
import time
import zenoh
from zenoh.net import config, SubInfo, Reliability, SubMode

# Run once at import time per zenoh instance
zenoh.init_logger()

# 128 byte packet for heartbeat, AGV -> RMF
HeartbeatPacket = np.array([i for i in range(128)], dtype=np.uint8)
# 4k packet for trajectories / tasks, RMF -> AGV
TaskPacket = np.array([0] * 4096, dtype=np.uint8)

class ZenohNode:

    def __init__(self):
        conf = {}
        # Docker router nodes client setup
        resource = '/zenoh/benchmark/topic'
        conf["peer"] = 'tcp/10.0.0.1:7447'
        conf["mode"] = 'client'

        print("Declaring session")
        self.session = zenoh.net.open(conf)
        print("Declaring resource")
        self.rid = self.session.declare_resource(resource)

    def __del__(self):
        self.session.close()


class ZenohPublisher(ZenohNode):

    def __init__(self):
        ZenohNode.__init__(self)
        print("Declaring publisher")
        self.publisher = self.session.declare_publisher(self.rid)

    def publish(self, message):
        #print("Publishing message")
        self.session.write(self.rid, message)

    def __del__(self):
        self.publisher.undeclare()



class ZenohSubscriber(ZenohNode):

    def __init__(self):
        ZenohNode.__init__(self)
        print("Declaring subscriber")
        sub_info = SubInfo(Reliability.Reliable, SubMode.Push)
        self.subscriber = self.session.declare_subscriber(self.rid, sub_info, self.callback)

    def callback(self, msg):
        print("Received message")

    def __del__(self):
        self.subscriber.undeclare()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--role',
            dest='role',
            type=str,
            required=True,
            help='Role of the node, publisher or subscriber',
            choices = ['pub', 'sub'])

    args = parser.parse_args()
    if args.role == 'pub':
        pub = ZenohPublisher()
        # Publish some stuff
        for i in range(10):
            pub.publish(HeartbeatPacket.tobytes())
            time.sleep(1)
    elif args.role == 'sub':
        sub = ZenohSubscriber()
        time.sleep(11)
