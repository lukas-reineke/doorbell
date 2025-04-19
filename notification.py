import os
import subprocess

import paho.mqtt.client as mqtt
import pygame

MQTT_BROKER = "192.168.3.12"
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


def on_message(_client, _userdata, msg):
    payload = msg.payload.decode()
    print(f"[MQTT] Received: {payload}")
    stop_music()
    play_sound()
    notify()


client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)
print(f"Listening on {MQTT_TOPIC} from {MQTT_BROKER}")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nExiting")
