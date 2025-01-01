# encoding:utf-8

import log
import time
import os
import requests

token = 'a1c54e811f1e4ce1b187921fc69cc388' #在pushplus网站中可以找到
title= '声光报警' #改成你要的标题内容

#define
#当发送weixinCnt次微信报警就需要声光报警
weixinCnt = 3
SPEAKER_SLEEP = 5
cnt = 0

def playmusic():
    os.system("mplayer alarm.m4a &")
    content = time.ctime() + ' 发出声光警报'
    url = 'http://www.pushplus.plus/send?token='+token+'&title='+title+'&content='+content
    response = requests.get(url)
    #print(response.text)
    if(response.status_code == 200):
        pass
    else:
        log.logger.error(f"发送声光报警消息不成功 {response.status_code}")

    
#出现两次
def speakerTask():
    global cnt
    log.logger.info("---enter speakerTask---")
    while True:
        if(cnt >= weixinCnt):
            log.logger.critical("发出声光报警")
            cnt = 0
            playmusic()
        time.sleep(SPEAKER_SLEEP)
        # 测试报警声能否正常播出
        #cnt = cnt + 1 

#playmusic()