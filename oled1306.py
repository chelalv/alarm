# encoding:utf-8
# https://learn.adafruit.com/monochrome-oled-breakouts/python-usage-2
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import time
import log
import temp, pir
import netifaces
import datetime
import os
import schedule

WIDTH = 128
HEIGHT = 64    
NOIP = "no IP"
FONT_SIZE = 20
IP_FONT_SIZE = 15
OLED_SLEEP = 3
DOWN_TIME = "20:00"

def shutdown_task():
    print("即将于 {DOWN_TIME} 关机...")
    os.system("sudo shutdown -h now")

def start_cron():
    result = subprocess.run(["timedatectl", "status"], capture_output=True, text=True)
    output = result.stdout
    # 检查输出中是否包含特定输出"
    if "System clock synchronized: yes" in output:
        schedule.every().day.at(DOWN_TIME).do(shutdown_task)
        return True
    else:
        return False
    
def getIP():
    try:
        # 优先无线网络(wlan0)
        interfaces = 'wlan0'
        addrs = netifaces.ifaddresses(interfaces)
        if netifaces.AF_INET in addrs:
            for addr_info in addrs[netifaces.AF_INET]:
                ip = addr_info['addr']
                if not ip.startswith('127.'):
                    return ip
                else:
                    return NOIP
        return NOIP
    except Exception as e:
        return NOIP

def oledTask():
    log.logger.info("---enter oledTask---")
    ip = getIP()
    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
    # Clear display.
    oled.fill(0)
    oled.show()
    font_ip = ImageFont.truetype("DejaVuSans.ttf", size=IP_FONT_SIZE)
    font = ImageFont.truetype("DejaVuSans.ttf", size=FONT_SIZE)
    height = font_ip.getbbox(ip)[3]
    cron_started = False
    while True:
        schedule.run_pending()
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (oled.width, oled.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        if(ip == NOIP):
            ip = getIP()
        elif(cron_started == False):
            if(start_cron() == True):
                cron_started = True
        draw.text((0, 0), ip,  font=font_ip, fill=255)
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        height2 = font.getbbox("test")[3]
        draw.text((0, height+2+height2), formatted_time, font=font, fill=255)
        tempe = round(temp.avg_temp,2)
        if(temp.flame_detected == True):
            if(pir.person_internal == True):
                text = f"m F t:{tempe}C"
                draw.text((0, height+2), text, font=font, fill=255)
            else:
                text = f"F t:{tempe}C"
                draw.text((0, height+2), text, font=font, fill=255)
        else:
            if(pir.person_internal == True):
                text = f"m t:{tempe}C"
                draw.text((0, height+2), text, font=font, fill=255)
            else:
                text = f"t:{tempe}C"
                draw.text((0, height+2), text, font=font, fill=255)
        # Display image
        oled.image(image)
        oled.show()
        image.close()
        time.sleep(OLED_SLEEP)