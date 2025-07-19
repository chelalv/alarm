# encoding:utf-8
# 用于客厅树莓派开启mqtt broker，以及订阅消息
import paho.mqtt.client as mqtt
import os
import subprocess
import schedule
import netifaces
import time

MQTT_SLEEP = 10
NOIP = "no IP"


DOWN_TIME = "20:05"
def getIP():
    try:
        # 优先无线网络(wlan0)
        interfaces = 'wlan0'
        addrs = netifaces.ifaddresses(interfaces)
        if netifaces.AF_INET in addrs:
            for addr_info in addrs[netifaces.AF_INET]:
                ip = addr_info['addr']
                if not ip.startswith('127.'):
                    return ip
                else:
                    return NOIP
        return NOIP
    except Exception as e:
        return NOIP

def shutdown_task():
    print(f"即将于 {DOWN_TIME} 关机...")
    os.system("sudo shutdown -h now")

def start_cron():
    result = subprocess.run(["timedatectl", "status"], capture_output=True, text=True)
    output = result.stdout
    # 检查输出中是否包含特定输出"
    if "System clock synchronized: yes" in output:
        schedule.every().day.at(DOWN_TIME).do(shutdown_task)
        return True
    else:
        return False

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}`")
    code = msg.payload.decode()
    if("pub power_on" == code):
        print("pub is on")
    elif("sub power_on" == code):
        print("sub is on")
    elif("alarm" == code):
        print("alarm")
        os.system("mplayer alarm.m4a &")


def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected with result code {rc}")
    # Subscribe, which need to put into on_connect
    # If reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("alarm/code", qos=1)
    # retain 为True 表示订阅者连接后会收到最近一次发布的消息
    client.publish("alarm/code", "sub power_on", qos=1, retain=True)  # qos=1保证至少送达一次

cron_started = False
ip = getIP()
while(ip == NOIP):
    ip = getIP()
    time.sleep(MQTT_SLEEP)
if(start_cron() == True):
    cron_started = True
else:
    print("cron start failed")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.will_set('alarm/code', b'sub power_off')
client.connect("localhost", 1883)
#client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

while True:
    schedule.run_pending()
    print("当前时间: ", time.strftime("%H:%M:%S"))
    time.sleep(MQTT_SLEEP)
