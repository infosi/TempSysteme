#PYTHON 3.6

import json
import time
import random
from datetime import datetime
import threading
from typing import Any

import paho.mqtt.client as mqtt

# Define constants
BROKER = "localhost"
PORT = 1883
TOPIC = "temperature/room"
CLIENT_ID = f"python-mqtt-tls-pub-sub-{random.randint(0, 1000)}"
SEUIL_MIN = 20
SEUIL_MAX = 25


# Function to publish temperature data for a specific room

# Callback functions
def on_connect(client: Any, userdata: Any, flags: Any, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected MQTT disconnection, return code {rc}")


def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")


# Function to publish temperature data for a specific room
def publish_temperature(mqttc, room_number):
    while True:
        data = {
            "date": datetime.now().isoformat(),
            "temperature": random.uniform(SEUIL_MIN, SEUIL_MAX),
        }
        mqttc.publish(f"{TOPIC}/{room_number}", json.dumps(data))
        print(f"Published temperature data for room {room_number}: {data}")
        time.sleep(1)


# Create MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message

# Connect to MQTT broker
mqttc.connect(BROKER, PORT, 60)

# Create threads for publishing temperature data for each room
rooms = [1, 2, 3, 4]
threads = [threading.Thread(target=publish_temperature, args=(mqttc, room)) for room in rooms]

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to finish (this will never happen in this code)
for thread in threads:
    thread.join()

# Disconnect from MQTT broker
mqttc.disconnect()

# Copyright (c) 2023 Infinicode

# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
