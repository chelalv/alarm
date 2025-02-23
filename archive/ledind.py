# encoding:utf-8
# https://gpiozero.readthedocs.io/en/stable/api_output.html
import time
import log
from gpiozero import LED
from gpiozero import PWMLED
from signal import pause
from datetime import datetime

import temp, pir

NORMAL = 0
WARNING = 1
ERROR = 2
PEOPLE = 3
LED_SLEEP = 5  #秒
LED_PULSE = 1 #呼吸 秒

def ledTask():
    log.logger.info("---enter ledTask---")
    #使用GPIO19，PIN35
    led = PWMLED(19)
    state = NORMAL
    led.pulse(1,LED_PULSE,None,True)
    while True:
        if(temp.flame_detected == True):
            # 检测到高温快速闪烁
            #led.close()
            # 没有人
            if(pir.person == False and state != ERROR):
                print("LED fire and nobody")
                led.blink(0.2,0.2,0,0,None,True)
                state = ERROR
            # 有人
            elif(pir.person == True and state != WARNING):
                print("LED fire and somebody")
                led.blink(0.5,0.5,0,0,None,True)
                state = WARNING
        elif(pir.person_internal == True and state != PEOPLE):
            # 有人经过
            print("somebody passby")
            led.on()
            state = PEOPLE
        elif(pir.person_internal == False and state != NORMAL):
            #led.close()
            # 正常工作一直呼吸
            print("LED normal")
            led.pulse(1,LED_PULSE,None,True)
            state = NORMAL
        time.sleep(LED_SLEEP)