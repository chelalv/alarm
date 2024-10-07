# encoding:utf-8
from ctypes import *
import time

#while True:
#    global flame_detected
flame_detected = False
print("---enter tempTask---\n")
#templist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
        #if(i%32 == 0 and i!=0):
        #    print("\n",end = '')
        #    if(i%64 == 0 and i!=0):
        #        print("\n",end = '')
        #print("%.2f " %(temp[i]),end = '')
        if(temp[i] < 100):
            templist[0] += 1
        elif(temp[i] >= 100 and temp[i] < 200):
            templist[1] += 1
        elif(temp[i] >= 200 and temp[i] < 300):
            templist[2] += 1
        elif(temp[i] >= 300 and temp[i] < 400):
            templist[3] += 1
        elif(temp[i] >= 400 and temp[i] < 500):
            templist[4] += 1
        """
        elif(temp[i] >= 500 and temp[i] < 600):
            templist[5] += 1
        elif(temp[i] >= 300 and temp[i] < 350):
            templist[6] += 1
        elif(temp[i] >= 350 and temp[i] < 400):
            templist[7] += 1
        elif(temp[i] >= 400 and temp[i] < 450):
            templist[8] += 1
        elif(temp[i] >= 450 and temp[i] < 500):
            templist[9] += 1
        elif(temp[i] >= 500 and temp[i] < 1000):
            templist[10] += 1
        elif(temp[i] >= 150 and temp[i] < 200):
            templist[11] += 1
        elif(temp[i] >= 200 and temp[i] < 300):
            templist[12] += 1
        elif(temp[i] >= 300 and temp[i] < 400):
            templist[13] += 1
        """
    print(templist)


    #if temp30_100 > 10:
        #global flame_detected
        #flame_detected = True
        #print("flame detected")


    templist = [0, 0, 0, 0, 0]

    time.sleep(3)

