import json
import os
import sys

import django

import paho.mqtt.client as mqtt


# Setup required before imports
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from iot.models import (
    Device,
    DeviceType,
    SensorData,
)


# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPICS = [("device/+/data", 0)]


def on_connect(client, userdata, flags, rc):
    print(f"Connected to {MQTT_BROKER} with result code {rc}")
    for topic, qos in MQTT_TOPICS:
        client.subscribe(topic, qos=qos)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        # e.g., payload = {"device_id": "sensor_A", "type": "temperature", "value": 22.5}
        device_name = payload.get("device_id")
        device_type_name = payload.get("type", "Unknown")
        value = payload.get("value", 0.0)

        device_type, _ = DeviceType.objects.get_or_create(name=device_type_name)
        device, _ = Device.objects.get_or_create(
            name=device_name,
            defaults={"device_type": device_type}
        )
        if not device.device_type:
            device.device_type = device_type
            device.save()

        SensorData.objects.create(device=device, value=value)

    except Exception as e:
        print("Error processing MQTT message:", e)


def start_mqtt_client():
    client = mqtt.Client()

    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    start_mqtt_client()
