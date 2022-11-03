#! /bin/python
# Name: bin_day_v3.py
# Author: gg
# Version 3.0
# Description: Query the Reading website API, format date, display bin information, act on button pressed to display wifi
# Calendar link: https://api.reading.gov.uk/api/collections/310012705
# Waveshare installation details: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Python_2
# Running on a Raspberry Pi Zero W + 8gb SD Card + 7.5inch E-Ink Display HAT 640x384 + Universal e-Paper Raw Panel Driver HAT + Mini Illuminated Momentary Pushbutton + 1kohm rezistor
# Eink: https://www.aliexpress.com/item/1005002297292956.html?spm=a2g0o.order_list.0.0.72991802a1h7yW
# HAT: https://thepihut.com/products/universal-e-paper-raw-panel-driver-hat?variant=32051318652990&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gclid=CjwKCAjw79iaBhAJEiwAPYwoCKitr6iBemNLsDU0WPlwXrg5jtMarHI3FOI726p-D7dMP21hJZwaOxoCRdMQAvD_BwE
# Button: https://thepihut.com/products/mini-illuminated-momentary-pushbutton-red-power-symbol


import requests
import re
import sys
import os
from datetime import date, datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import time
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO libraryhey
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5bc, epd7in5


def cal_query():

    url = 'https://api.reading.gov.uk/api/collections/310012705'
    page = ''
    mynewdate = date.today()

    try:
        page_long = requests.get(url)
        page_long = str(page_long.content)
        page = page_long[:605]
        # print(str(page.content)) #testing purposes
        bindate = re.search(r'\bread_date\":\s\"(\w+\s\w+\s\w+\s\w+)', page)
        bindate = bindate.group(1)

        mydate = re.search(r'\"date\":\s\"(\S+)', page)
        mydate = mydate.group(1)
        mynewdate = datetime.strptime(mydate, '%d/%m/%Y').date()
        #print(mynewdate)
    except:
        display_func('reach')
    else:
        try:
            if date.today()-timedelta(days=1) > mynewdate:
                display_func('error')
            else:
                # re-write the cronjob on a specific day
                if 'Recycling' in page:
                    display_func('bin_r', bindate)
                elif 'Domestic' in page:
                    display_func('bin', bindate)
                else:
                    display_func('error')
        except:
            display_func('error')
    return mynewdate

def display_func(bin_c, date=''): # mostly copied from epd_7in5_test.py examples
    try:
        epd = epd7in5bc.EPD()
        epdb = epd7in5.EPD()
        epd.init()
        epdb.init()
        # epd.Clear()
    except KeyboardInterrupt:
        epd7in5bc.epdconfig.module_exit()
        exit()
    else:
        if date:
            if bin_c == 'bin_r':
                font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
                HBlackimage = Image.new('1', (640, 384), 255)  # 640x384 image
                newimage = Image.open(os.path.join(picdir, f'{bin_c}.jpg'))  # red image
                HBlackimage.paste(newimage, (0, 0))
                drawblack = ImageDraw.Draw(HBlackimage)
                drawblack.text((35, 178), f'{date}', font=font24, fill=0)
                HRYimage = Image.open(os.path.join(picdir, f'{bin_c}_r.jpg'))  # red image
                epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
            else:
                font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
                HBlackimage = Image.new('1', (640, 384), 255)  # 640x384 image
                newimage = Image.open(os.path.join(picdir, f'{bin_c}.jpg'))  # red image
                HBlackimage.paste(newimage, (0, 0))
                drawblack = ImageDraw.Draw(HBlackimage)
                drawblack.text((35, 178), f'{date}', font=font24, fill=0)
                epdb.display(epdb.getbuffer(HBlackimage))
        else:
            HBlackimage = Image.open(os.path.join(picdir, f'{bin_c}.jpg'))  # 640x384 B&W image
            epdb.display(epdb.getbuffer(HBlackimage))
        epd.sleep()
    return


def main():
    time.sleep(20) # gives time for the raspberry to initialize including GPIO accesability
    GPIO.setwarnings(False)  # Ignore warnings
    GPIO.setmode(GPIO.BCM) # Use BCM pin numbering, that is what waveshare uses, so we have no conflicts
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 15 to be an input pin
    GPIO.add_event_detect(15, GPIO.RISING)

    bindate = cal_query()
    #print(bindate) #testing purposes
    while True:  # Run forever
        if date.today()-timedelta(days=1) > bindate:
            bindate = cal_query()
        time.sleep(0.5) #trying to further keep the CPU down
        if GPIO.event_detected(15): # only on event, this keeps the CPU down
            time.sleep(1)
            if GPIO.input(15) == GPIO.HIGH: # diffrent action if button is kept pressed for more than a sec
                GPIO.remove_event_detect(15)
                GPIO.cleanup()
                #print('button pressed') #testing purposes
                display_func('pic')
                bindate = cal_query()
                GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 15 to be an input pin
                GPIO.add_event_detect(15, GPIO.RISING)
            else:
                GPIO.remove_event_detect(15)
                GPIO.cleanup()
                display_func('wifi')
                bindate = cal_query()
                GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 15 to be an input pin
                GPIO.add_event_detect(15, GPIO.RISING)
        now = datetime.now()
        timp = now.strftime("%H:%M")
        if timp == '06:00': #noticed the gpios stop responding properly after a few days so this is to reset daily
            GPIO.remove_event_detect(15)
            GPIO.cleanup()
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 15 to be an input pin
            GPIO.add_event_detect(15, GPIO.RISING)
            time.sleep(70)

if __name__ == '__main__':
    main()