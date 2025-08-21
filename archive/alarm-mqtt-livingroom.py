# encoding:utf-8
# 用于客厅树莓派开启mqtt broker，以及订阅消息
import paho.mqtt.client as mqtt
import os
import subprocess
import schedule
import netifaces
import time
import log

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
    log.logger.info(f"即将于 {DOWN_TIME} 关机...")
    os.system("sudo shutdown -h now")

def start_cron():
    result = subprocess.run(["timedatectl", "status"], capture_output=True, text=True)
    output = result.stdout
    log.logger.info(output)
    # 检查输出中是否包含特定输出"
    if "System clock synchronized: yes" in output:
        log.logger.info("time is synchronized")
        schedule.every().day.at(DOWN_TIME).do(shutdown_task)
        return True
    else:
        log.logger.error("time is not synchronized")
        #os.system("sudo timedatectl set-ntp true")
        return False

def on_message(client, userdata, msg):
    log.logger.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` retain={msg.retain}")
    code = msg.payload.decode()
    if("pub power_on" == code):
        log.logger.info("pub is on")
    elif("sub power_on" == code):
        log.logger.info("sub is on")
    elif("alarm" == code):
        log.logger.info("alarm")
        os.system("mplayer alarm.m4a &")


def on_connect(client, userdata, flags, rc, properties):
    log.logger.info(f"Connected with result code {rc}")
    # Subscribe, which need to put into on_connect
    # If reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("alarm/code", qos=1)
    # retain 为True 表示订阅者连接后会收到最近一次发布的消息
    client.publish("alarm/code", "sub power_on", qos=1, retain=False)  # qos=1保证至少送达一次

log.logger.info("---start alarm-mqtt-livingroom.py---")
cron_started = False
ip = getIP()
while(ip == NOIP):
    log.logger.info("no IP get, get again and sleep 10s")
    ip = getIP()
    log.logger.info(ip)
    time.sleep(MQTT_SLEEP)
log.logger.info("IP is " + ip)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.will_set('alarm/code', b'sub power_off')
client.connect("localhost", 1883)
#client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

while True:
    if(cron_started == False):
        if(start_cron() == True):
            log.logger.info("cron started")
            cron_started = True
    else:
        try:
            schedule.run_pending()
        except Exception as e:
            log.logger.error(f"schedule run_pending error: {e}")
    #log.logger.info("当前时间: ", time.strftime("%H:%M:%S"))
    time.sleep(MQTT_SLEEP)
