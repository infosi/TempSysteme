# python 3.6

import json
import time
import random
from random import uniform
from datetime import datetime
import threading

import paho.mqtt.client as mqtt

seuil_max = 25.0
seuil_min = 22.0

CLIENT_ID = f'python-mqtt-tls-pub-sub-{random.randint(0, 1000)}'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def thread_pub(mqttc, numero_salle):
    while True:
        data = {"date": datetime.now().isoformat(),
                "temperature": uniform(seuil_min, seuil_max)}
        mqttc.publish("temperature/room/" + str(numero_salle), json.dumps(data))
        time.sleep(1)
        print(data)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.connect("localhost", 1883, 60)

room1 = threading.Thread(target=thread_pub, args=(mqttc, 1))
room2 = threading.Thread(target=thread_pub, args=(mqttc, 2))
room3 = threading.Thread(target=thread_pub, args=(mqttc, 3))
room4 = threading.Thread(target=thread_pub, args=(mqttc, 4))

room1.start()
room2.start()
room3.start()
room4.start()
