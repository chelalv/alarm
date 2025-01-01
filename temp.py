# encoding:utf-8
import time
import log
import serial
LEN_EMI = 4
LEN_DATA = 1544
LEN_TEMP_DATA = 1538
HEADER = 0x5A
POINT_NUM = 768

flame_detected = False

#define
#温度检测每TEMPSLEEP秒一次
TEMPSLEEP = 30 #秒
#COOK_TIME秒一直检测到火焰就认为在做饭了
COOK_TIME = 60 #秒
templist = [0, 0, 0, 0, 0]


def tempTask():
    log.logger.info("---enter tempTask---")
    global flame_detected
    ser = serial.Serial("/dev/ttyAMA4", 115200, timeout=3)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    cmd_get_emissivity =b"\xA5\x55\x01\xFB"
    ser.write(cmd_get_emissivity)
    #有rsp[0]=5a rsp[1]=5a rsp[2]=5f rsp[3]=13
    rsp = ser.read(4) 
    # 0x5a 0x5a 0x5f 0x13
    rsp_string =  ' '.join([hex(byte) for byte in rsp])
    print(f"emissivity data is {rsp_string}")
    cmd_get_data =b"\xA5\x35\x01\xDB"
    global templist

    while True:
        ser.write(cmd_get_data)
        rsp = ser.read(LEN_DATA)
        length = len(rsp)
        temp_length = int.from_bytes(rsp[2:4], byteorder='little')
        crc = int.from_bytes(rsp[-2:], byteorder='little')
        templist = [0, 0, 0, 0, 0]
        if(length != LEN_DATA):
            print(f"total lenght is {length} not {LEN_DATA}")
        elif(rsp[0] != HEADER or rsp[1] != HEADER):
            print(f"header data is {rsp[0]} not {HEADER}")
        elif(temp_length != LEN_TEMP_DATA):
            print(f"temperature data lenght is {temp_length} not {LEN_TEMP_DATA}")
        else:
            total = 0
            for i in range(0, length-2, 2):
                total += int.from_bytes(rsp[i:i+2], byteorder='little')
            total_bytes = total.to_bytes(4, 'little')
            if(total_bytes[0] != rsp[length-2] or total_bytes[1] != rsp[length-1]):
                print(f"crc is {hex(rsp[length-2])}{hex(rsp[length-1])}, The actual calculation result is {total_bytes[0:2]}")
            else:
                ta = int.from_bytes(rsp[-4:-2], byteorder='little')
                print(f"TA is {ta/100}")
                for i in range(0, POINT_NUM):
                    tp = int.from_bytes(rsp[i*2+4:i*2+6], byteorder='little')
                    if(tp < 100*100):
                        templist[0] += 1
                    elif(tp >= 100*100 and tp < 200*100):
                        templist[1] += 1
                    elif(tp >= 200*100 and tp < 300*100):
                        templist[2] += 1
                    elif(tp >= 300*100 and tp < 400*100):
                        templist[3] += 1
                    else:
                        templist[4] += 1
                print(templist)
                if(templist[1] >= 1 ):
                    #global flame_detected
                    flame_detected = True
                    print("flame detected")
                    log.logger.info(templist)
                else:
                    flame_detected = False
        time.sleep(TEMPSLEEP)
       

