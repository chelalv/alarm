# encoding:utf-8
from ctypes import *
import time
import log

flame_detected = False

#define
#温度检测每TEMPSLEEP秒一次
TEMPSLEEP = 30 #秒
#COOK_TIME秒一直检测到火焰就认为在做饭了
COOK_TIME = 60 #秒

def tempTask():
    global flame_detected
    start_cook = False
    start_time = 0
    end_time = 0
    log.logger.info("---enter tempTask---\n")
    #temp1 = temp2 = temp3=0
    templist = [0, 0, 0, 0, 0]
    mlx90640 = cdll.LoadLibrary('./libmlx90640.so')
    # 
    # mlx90640 will output 32*24 temperature array with chess mode
    #
    temp=(c_float*768)()
    ptemp=pointer(temp)
    while True:
        #print(f" flame_detected in tempTask {flame_detected}")
        mlx90640.get_mlx90640_temp(ptemp)
        for i in range(len(temp)):
            #if(i%16 == 0 and i!=0):
            #    print("\n",end = '')
            #print("%.2f " %(temp[i]),end = '')
            if(temp[i] < 100):
                templist[0] += 1
            elif(temp[i] >= 100 and temp[i] < 200):
                templist[1] += 1
            elif(temp[i] >= 200 and temp[i] < 300):
                templist[2] += 1
            elif(temp[i] >= 300 and temp[i] < 400):
                templist[3] += 1
            else:
                templist[4] += 1
        #print("\ntotal is "+ str(len(temp)) + ", temp below 30 is " + str(temp30) + \
        #      ", 30-100 is " + str(temp30_100) + ", over 100 is ", str(temp100) + ".\n")
        print(templist)

        if(templist[3] >= 1 or templist[4] >= 1):
            #global flame_detected
            flame_detected = True
            print("flame detected")
            #if(False == start_cook):
            #    startCook = True
            #    start_time = time.perf_counter()
        #没有检测到高温，再统计高温持续了多久
        else:
            flame_detected = False
            """
            if(True == start_cook):
                start_cook = False
                end_time = time.perf_counter()
                run_time = end_time - start_time
                if(run_time > COOK_TIME):
                    log.logger.info("正在做饭")
                    start_time = end_time = run_time = 0
            """
            

        #temp1 = temp2 = temp3 = 0
        templist = [0, 0, 0, 0, 0]
        
        time.sleep(TEMPSLEEP)
       

