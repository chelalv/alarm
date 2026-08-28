
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected with code {rc}")
    if rc == 0:
        print(f"Connected with code {rc}")
        client.publish("alarm/code", "power_on", qos=1, retain=False)  # qos=1保证至少送达一次
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print(f"Disconnected with code: {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.will_set('alarm/code', b'pub power_off')

client.connect("192.168.0.99", 1883, 60)
#client.connect("broker.hivemq.com", 1883, 60) 
client.loop_start()

while True:
    msg = input("Enter message to publish: ")
    if 'q' == msg or 'Q' == msg:
        exit()
    client.publish("alarm/code", msg, qos=1, retain=False)  # qos=1保证至少送达一次
    #time.sleep(2)