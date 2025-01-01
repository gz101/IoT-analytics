import os
from datetime import datetime
import json
import random
import time

import paho.mqtt.client as mqtt


BROKER = "127.0.0.1"
PORT = 1883
USERNAME = "mqtt_user"
PASSWORD = "securepassword"
TOPIC_TEMPLATE = "device/{device_id}/data"
DEVICE_ID = 1

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def generate_sensor_data():
    return {
        "device_id": DEVICE_ID,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "value": round(random.uniform(0.0, 100.0), 2)
    }

def main():
    client = mqtt.Client(client_id="SimulatedSensorDevice")
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT, 60)

    try:
        while True:
            sensor_data = generate_sensor_data()
            topic = TOPIC_TEMPLATE.format(device_id=DEVICE_ID)
            payload = json.dumps(sensor_data)
            client.publish(topic, payload)
            print(f"Published: {payload} to topic {topic}")
            time.sleep(5)

    except KeyboardInterrupt:
        print("Simulation stopped.")
        client.disconnect()

if __name__ == "__main__":
    main()
