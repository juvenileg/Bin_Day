#! /bin/python
# Name: bin_calendar.py
# Author: gg
# Version 1.0
# Description: This is for codetesting purposes

import requests
import re
from datetime import date, datetime


def cal_query():

    try:
        url = f'http://numbersapi.com/{date.today().strftime("%m")}/{date.today().strftime("%d")}/date'
        page = requests.get(url)
        quote = page.text
    except:
        quote = 'No quote found'

    print(quote)
    nquote = []
    nquote = re.findall(r'(.{1,55}\b)', quote)
    print(nquote)
    quote = '\n'.join(nquote)
    print(quote)
    url = 'https://api.reading.gov.uk/rbc/mycollections/40%20Windrush%20Way%20Reading,%20RG302NQ'
    mynewdate = date.today()
    try:
        page = requests.get(url)
        data = page.json()
        mynewdate = datetime.strptime(data['Collections'][0]['Date'], "%d/%m/%Y %H:%M:%S").date()
        bindate = mynewdate.strftime("%A, %d %B")
        print(bindate)
    except:
        print('error')
    else:
        print(date.today())
        if date.today() < mynewdate:
            print('True')
    try:
        if date.today() > mynewdate:
            print('error')
        else:
            if 'Recycling' in data['Collections'][1]['Service']:
                print('recycle')
            elif 'Domestic' in data['Collections'][0]['Service']:
                print('somestiv')
            else:
                print('error')
    except:
        print('error')


def main():  # This function is never used, test purpose only for when running the script
    cal_query()


if __name__ == '__main__':
    main()
