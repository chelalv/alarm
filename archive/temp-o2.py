# encoding:utf-8
# 使用自己写的libsensor库。
from ctypes import *
import time
import log

flame_detected = False

#define
#温度检测每TEMPSLEEP秒一次
TEMPSLEEP = 30 #秒
#COOK_TIME秒一直检测到火焰就认为在做饭了
COOK_TIME = 60 #秒
templist = [0, 0, 0, 0, 0]


def tempTask():
    global flame_detected
    start_cook = False
    start_time = 0
    end_time = 0
    log.logger.info("---enter tempTask---\n")
    global templist
    mlx90640 = cdll.LoadLibrary('./libsensor.so')
    #mlx90640.sensorInit(0,0)
    # 
    # mlx90640 will output 32*24 temperature array with chess mode
    #
    while True:
        #print(f" flame_detected in tempTask {flame_detected}")
        templist[1] = mlx90640.getTemp(0, 0)
        print(templist)
        if(templist[1] >= 1 ):
            flame_detected = True
            print("flame detected")
            log.logger.info(templist)
        #没有检测到高温
        else:
            flame_detected = False
        #temp1 = temp2 = temp3 = 0
        templist = [0, 0, 0, 0, 0]
        
        time.sleep(TEMPSLEEP)
       

