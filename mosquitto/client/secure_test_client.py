#!/usr/bin/python3

import numpy as np
import os
import ssl
import time
import paho.mqtt.client as mqtt


client_id = 'robot1'
topic_name = '/mqtt1/benchmark/topic'  # same length as zenoh resource ID name

mqttc = mqtt.Client(client_id)

certs_path='../broker/certs'
ca_certs = os.path.join(certs_path, 'minica.pem')
certfile = os.path.join(certs_path, 'localhost', 'cert.pem')
keyfile = os.path.join(certs_path, 'localhost', 'key.pem')

mqttc.tls_set(
    ca_certs=ca_certs,
    certfile=certfile,
    keyfile=keyfile,
    cert_reqs=ssl.CERT_REQUIRED)

mqttc.username_pw_set('user', 'password')

mqttc.connect('localhost', 8883)  # can set keepalive here

# loop_start() creates a sending thread which will automatically generate
# keepalives as well as reconnect as needed
mqttc.loop_start()

HeartbeatPacket = np.array([i for i in range(128)], dtype=np.uint8).tobytes()
TaskPacket = np.array([0] * 4096, dtype=np.uint8).tobytes()

delay_seconds = 1.0

try:
    while True:
        info = mqttc.publish(topic_name, TaskPacket)
        info.wait_for_publish()
        time.sleep(delay_seconds)

except KeyboardInterrupt:
    pass

mqttc.disconnect()
print('goodbye')
