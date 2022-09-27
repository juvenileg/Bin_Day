#! /bin/python
# Name: bin_calendar.py
# Author: gg
# Version 1.0
# Description: Strip calendar data
# Calendar link: https://api.reading.gov.uk/api/collections/310012705
# Waveshare installation details: https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Python_2

import requests
import re
from screen import display_func
from datetime import date, datetime


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


def main():  # This function is never used, test purpose only for when running the script
    cal_query()


if __name__ == '__main__':
    main()
