#! /bin/python
# -*- coding:utf-8 -*-
# Name: screen.py
# Author: gg
# Version 1.0
# Description: This program will return the image on the screen

import sys
import os
import time
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5bc, epd7in5
from PIL import Image, ImageDraw, ImageFont


def display_func(bin_c, date=''):
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
        time.sleep(10)  # This image will disappear after 10 seconds
        epd.sleep()
    return


def main():
    display_func('bin_r', 'Wednesday 28th of September')


if __name__ == '__main__':
    main()
    sys.exit(0)
