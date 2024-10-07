# encoding:utf-8
from ctypes import *
import time

from gpiozero import DigitalInputDevice
from signal import pause
from datetime import datetime

person =  False
person_internal = False
startTime = 0

#define
#人检测PIR_SLEEP秒一次
PIR_SLEEP = 5  #秒

#只要PIR_TIME秒之内检测到有人就认为有人，1分钟之内都没有检测到动作，就认为没有人
PIR_TIME = 15

def someone_near():
    global person
    global person_internal
    person = True
    person_internal = True
    print("someone near")


def someone_left():
    global person_internal
    global startTime
    person_internal = False
    print("someone left")
    #检测到人离开，开始倒计时
    startTime = time.perf_counter()

print("---enter pirTest---\n")
#使用的是11脚GPIO0
#pir = DigitalInputDevice(pin = 17)
#RPI4使用13脚GPIO 27
pir = DigitalInputDevice(pin = 27)
pir.when_activated = someone_near
pir.when_deactivated = someone_left

print(pir.value)
if(pir.value == 1):
    person = True


while True:
    if(False == person_internal and startTime != 0):
        endTime = time.perf_counter()
        runTime = endTime - startTime
        print(runTime)
        if(runTime > PIR_TIME):
            person = False
            startTime = endTime = runTime = 0
            print(f"已经{PIR_TIME}秒没有动静了")
    time.sleep(PIR_SLEEP)