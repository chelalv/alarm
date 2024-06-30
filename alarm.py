# encoding:utf-8
import threading
import os
import time
import logging
import sys
from datetime import datetime

#from queue import Queue

from temp import tempTask
from pir import pirTask
from weixin import weixinTask
from speaker import speakerTask

import temp, pir, weixin,log

program_exit = False

#define
#LEVEL = logging.INFO
#主线程睡眠MAIN_SLEEP秒
MAIN_SLEEP = 3

def keyboardTask():
    global program_exit
    while True:
        key = input("press q to exit\n")
        if(key == 'q' or key == 'Q'):
            print("program exit")
            program_exit = True
        else:
            print(f"your input is {key}")
        time.sleep(3)


if __name__ == "__main__":


    log.logger.info("ID of process running main program: {}".format(os.getpid()))
    log.logger.info("Main thread name: {}".format(threading.current_thread().name))

    t1 = threading.Thread(target=weixinTask, name='weixin')
    t2 = threading.Thread(target=tempTask, name='temp')
    t3 = threading.Thread(target=pirTask, name='pir')
    t4 = threading.Thread(target=keyboardTask, name = "keyboard")
    t5 = threading.Thread(target=speakerTask, name = "speaker")

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True
    t5.daemon = True
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()


    while True:
        #主线程先睡眠，保证能拿到新的传感器值
        time.sleep(MAIN_SLEEP)
        #print(f"program_exit is {program_exit}")
        #print(f" flame_detected {temp.flame_detected}, person {person}, flag {weixin.weixinFlag}")
        #print(f" flame_detected {flame_detected}, person {person}, flag {weixinFlag}")
        if(program_exit == True):
            exit()
        if(temp.flame_detected == True and pir.person == False):
            #print("这时候需要报警检测到高温并且人不在旁边")
            if(weixin.weixinFlag == False):
                weixin.weixinFlag = True
            else:
                #print("暂时无法报警，因为已经报警过一次了，需要等待30秒之后再报警")
                pass
        elif(temp.flame_detected == True and pir.person == True):
            print("这时候不需要报警因为人在旁边正在做饭")
            pass
        elif(temp.flame_detected == False and pir.person == True):
            #print("这时候不需要报警可能只是人从旁边走过")
            #log.logger.info("有人在")
            pass
        elif(temp.flame_detected == False and pir.person == False):
            #print("无任何情况不需要报警")
            pass
        #time.sleep(MAIN_SLEEP)

        