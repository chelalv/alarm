# encoding:utf-8

import time
import os
import threading


def playmusic():
    os.system("mplayer alarm.m4a &")

def speakerTask():
    weixinCnt = 3
    SPEAKER_SLEEP = 5
    cnt = 0
    while True:
        if(cnt >= weixinCnt):
            cnt = 0
            playmusic()
        time.sleep(SPEAKER_SLEEP)
        cnt = cnt + 1

if __name__ == "__main__":
    t5 = threading.Thread(target=speakerTask, name = "speaker")
    t5.daemon = True
    t5.start()
    while True:
        time.sleep(5)
