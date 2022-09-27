#! /bin/python
# Name: bin_calendar.py
# Author: gghica
# Version 1.0
# Description: Strip calendar data
# Calendar link: https://api.reading.gov.uk/api/collections/310012705

import requests
import re
from screen import display_func
from datetime import date, datetime

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

