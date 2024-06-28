# encoding:utf-8

import log
import time

#define
#当发送weixinCnt次微信报警就需要声光报警
weixinCnt = 3
SPEAKER_SLEEP = 5
cnt = 0

def playmusic():
    pass
#出现两次
def speakerTask():
    global cnt
    log.logger.info("---enter speakerTask---\n")
    while True:
        if(cnt >= weixinCnt):
            log.logger.critical("发出声光报警")
            cnt = 0
            playmusic()
        time.sleep(SPEAKER_SLEEP)
    