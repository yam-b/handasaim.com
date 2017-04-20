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


def b(url):
    news = bs(requests.get(url).content, 'lxml').find('marquee')
    return [i for i in news.find_all('b') if TEXT_TO_FIND in i.text][0]


def news_list(url):
    news = bs(requests.get(url).content, 'lxml').find('marquee')
    list = []
    for i, item in enumerate(news.find_all('b')):
        try:
            date = item.find_previous_sibling('sup').text[1:-1]
        except:
            date = ''
        try:
            title = item.text.strip()
        except:
            title = u'פריט חדשות מספר ' + str(i)
        try:
            link = item.find_next_sibling('a')['href'].strip()
        except:
            link = ''
        try:
            description = item.next_sibling.strip()
        except:
            description = ''
        dictionary = {'date': date, 'title': title, 'link': link, 'description': description}
        a = 1
        for j in range(len(list)):
            if list[j][0]['date'] == date:
                list[j].append(dictionary)
                a = 0
        if a: list.append([dictionary])
    return list


def column_to_list(column):
    l = list(column)
    lst = []
    for i in column:
        if pd.isnull(i):
            i = ''
        lst.append(i)
    return lst

def to_table(url):
    sheet = pd.ExcelFile(url).parse(0)
    return [(['<small style="color:#a1a4a5">{}</small><br><b>{}</b><br><small style="color:#a1a4a5">{}</small>'.format(
        school_time(i)[0], i, school_time(i)[1])] if i + 1 else []) + column_to_list(sheet.iloc[i + 1, LEFT_CUT:]) for i
            in
            range(UP_CUT - 1, len(sheet.index) - 1)]


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
        '12': u'דצמבר'
    }[month]


def to_heb_day(day):
    return {
        '0': u'ראשון',
        '1': u'שני',
        '2': u'שלישי',
        '3': u'רביעי',
        '4': u'חמישי',
        '5': u'שישי',
        '6': u'שבת'
    }[day]


def school_time(time):
    return {
        0: ['07:45', '8:30'],
        1: ['8:30', '9:15'],
        2: ['9:15', '10:00'],
        3: ['10:15', '11:00'],
        4: ['11:00', '11:45'],
        5: ['12:10', '12:55'],
        6: ['12:55', '13:40'],
        7: ['13:50', '14:35'],
        8: ['14:35', '15:25'],
        9: ['15:30', '16:15'],
        10: ['16:15', '17:00'],
        11: ['17:00', '17:45'],
        12: ['17:45', '18:30']
    }[time]


def index(request):
    error = 0
    # local = os.path.join(BASE_DIR, 'handaschedule/schedule.xlsx')
    try:
        title = b(URL).text.strip()
        day = title[-4:-2]
        month = '0' + title[-1]
        link = b(URL).find_next_sibling('a')['href'].strip()
        table = to_table(link)  # ONLINE: to_table(link) OFFLINE: to_table(local)
        date = b(URL).find_previous_sibling('sup').text[1:-1]
        date = date[:2] + u' ב' + to_heb_month(date[3:5])
    except:
        title = 'אין מערכת'
        day = datetime.date.today().strftime('%d')
        month = datetime.date.today().strftime('%m')
        link = '#'
        table = []
        date = ''
        error = 1
    try:
        description = b(URL).next_sibling.strip()
    except:
        description = DEFAULT_INFO
    try:
        list = news_list(URL)
    except:
        list = []
    weekday = datetime.datetime.strptime(day + month + str(datetime.datetime.now().year), '%d%m%Y').date().strftime(
        '%w')
    time = u'יום ' + to_heb_day(weekday) + ', ' + day + u' ב' + to_heb_month(month)
    lst = [i for i in range(5, 100)]
    return render(request, 'handaschedule/index.html',
                  {'text': TEXT_TO_FIND, 'url': URL, 'title': title, 'info': description, 'link': link, 'time': time,
                   'date': date, 'table': table,
                   'error': error, 'news_list': list})
