#!/usr/bin/python3

import numpy as np
import time
import paho.mqtt.client as mqtt

client_id = 'robot1'
topic_name = '/mqtt1/benchmark/topic'  # same length as zenoh resource ID name

mqttc = mqtt.Client(client_id, True)
mqttc.connect('localhost', 1883)

# loop_start() creates a sending thread which will automatically generate
# keepalives as well as reconnect as needed
mqttc.loop_start()

HeartbeatPacket = np.array([i for i in range(128)], dtype=np.uint8).tobytes()
TaskPacket = np.array([0] * 4096, dtype=np.uint8).tobytes()

delay_seconds = 1.0

try:
    while True:
        info = mqttc.publish(topic_name, HeartbeatPacket)
        info.wait_for_publish()
        time.sleep(delay_seconds)


except KeyboardInterrupt:
    pass

mqttc.disconnect()
print('goodbye')
