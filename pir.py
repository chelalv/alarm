# encoding:utf-8
import time
import log
from gpiozero import DigitalInputDevice
from signal import pause
from datetime import datetime

person =  False
#changed = False

#define
#人检测PIR_SLEEP秒一次
#只要PIR_SLEEP秒之内检测到有人就认为有人，1分钟之内都没有检测到动作，就认为没有人
PIR_SLEEP = 60  #秒

def someone_near():
    global person
    #global changed
    #changed = True
    person = True
    print("someone near")

def someone_left():
    #global person
    #print("someone left")
    pass


def pirTask():
    log.logger.info("---enter pirTask---\n")
    #使用的是11脚GPIO0
    pir = DigitalInputDevice(pin = 17)
    pir.when_activated = someone_near
    pir.when_deactivated = someone_left

    global person
    #global changed
    while True:
        #if(True == changed):
        #    person = True
        time.sleep(PIR_SLEEP)
        person = False





