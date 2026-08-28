# encoding:utf-8
# https://learn.adafruit.com/monochrome-oled-breakouts/python-usage-2
# https://pypi.org/project/netifaces/
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import time
import netifaces
import datetime
import os
import schedule

WIDTH = 128
HEIGHT = 64    
NORMAL_MODE = "normal"
MAN_MODE = "only man"
MANDF_MODE = "man and fire"
FIRE_MODE = "only fire"
NOIP = "no IP"
FONT_SIZE = 15
IP_FONT_SIZE = 15
OLED_SLEEP = 3
DOWN_TIME = "20:25"

def shutdown_task():
    print("即将于 {DOWN_TIME} 关机...")
    os.system("sudo shutdown -h now")

def getIP():
    ip = [NOIP,NOIP]
    try:
        interfaces = ['wlan0','eth0']
        addrs = netifaces.ifaddresses(interfaces[0])
        ipv4_address = addrs.get(netifaces.AF_INET)
        if ipv4_address:
            # ipv4_address is a list of dictionaries, typically containing one element
            ip[0] = ipv4_address[0]['addr']
        addrs = netifaces.ifaddresses(interfaces[1])
        ipv4_address = addrs.get(netifaces.AF_INET)
        if ipv4_address:
            # ipv4_address is a list of dictionaries, typically containing one element
            ip[1] = ipv4_address[0]['addr']
        return ip
    except Exception as e:
        return ip

def start_cron():
    result = subprocess.run(["timedatectl", "status"], capture_output=True, text=True)
    output = result.stdout
    # 检查输出中是否包含特定输出"
    if "System clock synchronized: yes" in output:
        schedule.every().day.at(DOWN_TIME).do(shutdown_task)
        return True
    else:
        return False
    
while True:
    ip = getIP()
    # Use for I2C.
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)
    # Clear display.
    oled.fill(0)
    oled.show()
    font = ImageFont.truetype("DejaVuSans.ttf", size=FONT_SIZE)
    height = font.getbbox(NOIP)[3]
    while True:
        schedule.run_pending()
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (oled.width, oled.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        if(ip[0] == NOIP and ip[1] == NOIP):
            ip = getIP()
        draw.text((0, 0), ip[0],  font=font, fill=255)
        draw.text((0, height), ip[1],  font=font, fill=255)
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        draw.text((0, height*2+2), formatted_time, font=font, fill=255)
        # Display image
        oled.image(image)
        oled.show()
        image.close()
        time.sleep(OLED_SLEEP)