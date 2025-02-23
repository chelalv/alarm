# encoding:utf-8
# https://learn.adafruit.com/monochrome-oled-breakouts/python-usage-2
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
import time
import log
import temp, pir

WIDTH = 128
HEIGHT = 64    
NORMAL_MODE = "normal"
MAN_MODE = "only man"
MANDF_MODE = "man and fire"
FIRE_MODE = "only fire"
NOIP = "no IP"
FONT_SIZE = 20
IP_FONT_SIZE = 15
OLED_SLEEP = 3

def getIP():
    cmd = "hostname -I"
    ret = subprocess.check_output(cmd, shell = True)
    ip = ret.decode('utf-8').split(' ', 2)[0]
    if(len(ip) != 0):
        return ip
    else:
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
    while True:
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (oled.width, oled.height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Load default font.
        # Draw Some Text
        if(ip == NOIP):
            ip = getIP()
        draw.text((0, 0), ip,  font=font_ip, fill=255)
        if(temp.flame_detected == True):
            if(pir.person_internal == True):
                draw.text((0, height+2), "man and fire", font=font, fill=255)
            else:
                draw.text((0, height+2), "only fire", font=font, fill=255)
        else:
            if(pir.person_internal == True):
                draw.text((0, height+2), "only man", font=font, fill=255)
            else:
                draw.text((0, height+2), "normal", font=font, fill=255)
        # Display image
        oled.image(image)
        oled.show()
        image.close()
        time.sleep(OLED_SLEEP)