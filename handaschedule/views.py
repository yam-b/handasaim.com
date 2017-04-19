# -*- coding: utf-8 -*-
import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from django.shortcuts import render

URL = 'http://www.handasaim.co.il'
TEXT_TO_FIND = u'מערכת שעות'
UP_CUT = 0
LEFT_CUT = 1
DEFAULT_INFO = u''


def b(link):
    news = bs(requests.get(link).content, 'lxml').find('marquee')
    return [i for i in news.find_all('b') if TEXT_TO_FIND in i.text][0]


def to_table(url):
    sheet = pd.ExcelFile(url).parse(0)
    return [sheet.iloc[i, LEFT_CUT:] for i in range(UP_CUT, len(sheet.index))]


def to_heb_month(month):
    return {
        '01': u'ינואר',
        '02': u'פברואר',
        '03': u'מרץ',
        '04': u'אפריל',
        '05': u'מאי',
        '06': u'יוני',
        '07': u'יולי',
        '08': u'אוגוסט',
        '09': u'ספטמבר',
        '10': u'אוקטובר',
        '11': u'נובמבר',
        '12': u'דצמבר',
    }[month]


def index(request):
    error = 0
    # local = os.path.join(BASE_DIR, 'handaschedule/schedule.xlsx')
    try:
        title = b(URL).text.strip()
        day = title[-5:-2]
        month = '0' + title[-1]
        link = b(URL).find_next_sibling('a')['href'].strip()
        table = to_table(link)  # ONLINE: to_table(link) OFFLINE: to_table(local)
        upload_time = b(URL).find_previous_sibling('sup').text[1:-1]
        upload_time = upload_time[:2] + u' ב' + to_heb_month(upload_time[3:5])
    except:
        title = 'מערכת שעות'
        day = datetime.date.today().strftime('%d ')
        month = datetime.date.today().strftime('%m')
        link = '#'
        table = []
        upload_time = ''
        error = 1
    try:
        info = b(URL).next_sibling.strip()
    except:
        info = DEFAULT_INFO
    time = day + u' ב' + to_heb_month(month)
    return render(request, 'handaschedule/index.html',
                  {'text': TEXT_TO_FIND, 'url': URL, 'title': title, 'info': info, 'link': link, 'time': time,
                   'upload_time': upload_time, 'table': table,
                   'error': error})
