# encoding:utf-8
import time
import requests
import log, speaker
from gpiozero import CPUTemperature

weixinFlag = False
sentFlag = False
start_time = 0

token = 'a1c54e811f1e4ce1b187921fc69cc388' #在pushplus网站中可以找到
title= '报警' #改成你要的标题内容

#define
#发送一次报警后sendTimer秒之后才能再发送报警
sendTimer = 60
#发送报警信息每WEIXIN_SLEEP秒就需要查看要不要发微信报警
WEIXIN_SLEEP = 2

HEARTBEATTIME = 60 * 60 


def sendMsg():
    global sentFlag, start_time
    content = time.ctime() + ' 检测到高温并且人不在旁边'
    url = 'http://www.pushplus.plus/send?token='+token+'&title='+title+'&content='+content
    response = requests.get(url)
    #print(response.text)
    if(response.status_code == 200):
        sentFlag = True
        start_time = time.perf_counter()
        speaker.cnt += 1
    else:
        log.logger.error(f"发送消息不成功 {response.status_code}")



def weixinTask():
    global weixinFlag, start_time, sentFlag, sendTimer
    log.logger.info("---enter weixinTask---\n")
    heartbeet = False
    cpu = CPUTemperature()
    while True:
        #print("weixinTask")
        #print(f"weixinFlag in weixinTask {weixinFlag}, sentFlag {sentFlag}")
        if(weixinFlag == True and sentFlag == False):
            log.logger.info("发送报警信息到微信")
            sendMsg()
        end_time = time.perf_counter()
        run_time = end_time - start_time
        if(run_time > sendTimer and sentFlag == True):
            log.logger.info("报警已经过去{}秒".format(sendTimer) + "准备下一次报警")
            sentFlag = False
            weixinFlag = False
        if(False == heartbeet):
            heartbeetStart = time.perf_counter()
            heartbeet = True
        heartbeetStop = time.perf_counter()
        if(heartbeetStop - heartbeetStart > HEARTBEATTIME):
            temp = cpu.temperature
            log.logger.info(f"heartbeat {temp}")
            heartbeet = False
        time.sleep(WEIXIN_SLEEP)