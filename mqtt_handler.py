import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MONGO_URI

client = MongoClient(MONGO_URI)
db = client["drone_survey"]

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    db.missions.update_one(
        {"mission_id": data["mission_id"]},
        {"$set": {"status": data["status"], "progress": data["progress"]}}
    )

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()
