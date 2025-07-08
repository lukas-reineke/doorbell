import os
import subprocess
import time

import paho.mqtt.client as mqtt
import pygame

MQTT_BROKER = "192.168.3.4"
MQTT_TOPIC = "home/doorbell/ring"
SOUND_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "notification.mp3")

pygame.mixer.init()
pygame.mixer.music.load(SOUND_FILE)
pygame.mixer.music.set_volume(1.0)


def notify():
    subprocess.run(["notify-send", "🔔 Doorbell", "Someone is at the door!"])


def stop_music():
    subprocess.run(["playerctl", "pause"])


def play_sound():
    pygame.mixer.music.play()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ Failed to connect, return code {rc}")


def on_disconnect(client, userdata, rc):
    print(f"⚠️ MQTT Disconnected (rc={rc}) – retrying...")
    reconnect(client)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[MQTT] Received: {payload}")
    stop_music()
    play_sound()
    notify()


def reconnect(client):
    while True:
        try:
            client.reconnect()
            print("🔄 Reconnected to MQTT")
            break
        except Exception as e:
            print(f"Retry failed: {e}")
            time.sleep(5)


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print(f"🔌 Connecting to {MQTT_BROKER}...")
client.connect(MQTT_BROKER, 1883, 60)

try:
    client.loop_forever(retry_first_connection=True)
except KeyboardInterrupt:
    print("\n👋 Exiting")
