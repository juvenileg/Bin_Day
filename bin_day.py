#! /bin/python
# Name: bin_dayr.py
# Author: gg
# Version 1.0
# Description: Strip calendar data
# Calendar link: https://api.reading.gov.uk/api/collections/310012705
# Waveshare installation details: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Python_2

import requests
import re
import sys
import os
from PIL import Image, ImageDraw, ImageFont
from screen import display_func
from datetime import date, datetime
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO libraryhey
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5bc, epd7in5


def cal_query():

    url = 'https://api.reading.gov.uk/api/collections/310012705'

    page_long = requests.get(url)
    page_long = str(page_long.content)
    page = page_long[:605]

    # print(str(page.content))
    bindate = re.search(r'\bread_date\":\s\"(\w+\s\w+\s\w+\s\w+)', page)
    bindate = bindate.group(1)

    mydate = re.search(r'\"date\":\s\"(\S+)', page)
    mydate = mydate.group(1)
    mynewdate = datetime.strptime(mydate, '%d/%m/%Y').date()

    if date.today() > mynewdate:
        display_func('error')
    else:
        # re-write the cronjob on a specific day
        if 'Recycling' in page:
            display_func('bin_r', bindate)
        elif 'Domestic' in page:
            display_func('bin', bindate)
        else:
            display_func('error')

def display_func(bin_c, date=''):
    try:
        print(datetime.today())
        epd = epd7in5bc.EPD()
        epdb = epd7in5.EPD()
        epd.init()
        epdb.init()
        # epd.Clear()
        print(datetime.today())
    except KeyboardInterrupt:
        epd7in5bc.epdconfig.module_exit()
        exit()
    else:
        print(datetime.today())
        if date:
            if bin_c == 'bin_r':
                font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
                HBlackimage = Image.new('1', (640, 384), 255)  # wifi.jpg is 640x384 image
                newimage = Image.open(os.path.join(picdir, f'{bin_c}.jpg'))  # red image
                HBlackimage.paste(newimage, (0, 0))
                drawblack = ImageDraw.Draw(HBlackimage)
                drawblack.text((35, 178), f'{date}', font=font24, fill=0)
                HRYimage = Image.open(os.path.join(picdir, f'{bin_c}_r.jpg'))  # red image
                epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
            else:
                font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
                HBlackimage = Image.new('1', (640, 384), 255)  # wifi.jpg is 640x384 image
                newimage = Image.open(os.path.join(picdir, f'{bin_c}.jpg'))  # red image
                HBlackimage.paste(newimage, (0, 0))
                drawblack = ImageDraw.Draw(HBlackimage)
                drawblack.text((35, 178), f'{date}', font=font24, fill=0)
                epdb.display(epdb.getbuffer(HBlackimage))
        else:
            HBlackimage = Image.open(os.path.join(picdir, f'{bin_c}.jpg'))  # wifi.jpg is 640x384 image
            HRYimage = Image.open(os.path.join(picdir, f'{bin_c}_r.jpg'))  # red image
            epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
        epd.sleep()
        print(datetime.today())
    return


def main():  # This function is never used, test purpose only for when running the script
    GPIO.setwarnings(False)  # Ignore warning for now
    # GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin

    while True:  # Run forever
        if GPIO.input(15) == GPIO.HIGH:
            GPIO.cleanup()
            print('button pressed')
            display_func('wifi')
            cal_query()
            GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin


if __name__ == '__main__':
    main()