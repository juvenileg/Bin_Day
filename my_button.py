#! /bin/python
# Name: .py
# Author: gg
# Version 1.0
# Description:
import time

from screen import display_func
from bin_calendar import cal_query
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library


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
