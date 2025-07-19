# encoding:utf-8

import log
import time
import os
import requests
import paho.mqtt.client as mqtt


token = 'a1c54e811f1e4ce1b187921fc69cc388' #在pushplus网站中可以找到
title= '声光报警' #改成你要的标题内容

#define
#当发送weixinCnt次微信报警就需要声光报警
weixinCnt = 3
SPEAKER_SLEEP = 5
cnt = 0

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print(f"Connected with code {rc}")
        client.subscribe("alarm/code", qos=1)
        # retain 为True 表示订阅者连接后会收到最近一次发布的消息
        client.publish("alarm/code", "pub power_on", qos=1, retain=True)  # qos=1保证至少送达一次        
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, flags, rc, properties):
    print(f"Disconnected with code: {rc}")

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}`")
    code = msg.payload.decode()
    if("pub power_on" == code):
        print("pub is on")
    elif("sub power_on" == code):
        print("sub is on")

def playmusic():
    os.system("mplayer alarm.m4a &")
    content = time.ctime() + ' 发出声光警报'
    url = 'http://www.pushplus.plus/send?token='+token+'&title='+title+'&content='+content
    response = requests.get(url)
    #print(response.text)
    if '200' not in response.text:
        log.logger.error(f"发送声光报警消息不成功 {response.status_code}")

    
#出现两次
def speakerTask():
    global cnt
    log.logger.info("---enter speakerTask---")
    # clean_session=False 保持会话持久化：重连后自动恢复订阅列表和未接收的QoS1/2消息‌
    client = mqtt.Client(client_id="alarm_pub", 
                         clean_session=False, 
                         callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.will_set('alarm/code', b'pub power_off')
    # The client will automatically retry connection. 
    # Between each attempt it will wait a number of seconds between min_delay and max_delay.
    client.reconnect_delay_set(min_delay=1, max_delay=600)  # 设置重连间隔范围
    try:
       client.connect("192.168.0.99", 1883, 60)
    except Exception as e:
       print(f"连接异常: {e}")
    client.loop_start()
    while True:
        if(cnt >= weixinCnt):
            log.logger.critical("发出声光报警")
            cnt = 0
            playmusic()
            client.publish("alarm/code", "alarm", qos=1, retain=False)  # qos=1保证至少送达一次
        time.sleep(SPEAKER_SLEEP)
        # 测试报警声能否正常播出
        #cnt = cnt + 1 

#playmusic()