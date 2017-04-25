# -*- coding: utf-8 -*-
import datetime as dt

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs

URL = 'http://www.handasaim.co.il'
TEXT_TO_FIND = u'מערכת שעות'
UP_CUT = 0
LEFT_CUT = 1
DEFAULT_INFO = u''
HEB_WEEKDAY = (
    u'ראשון',
    u'שני',
    u'שלישי',
    u'רביעי',
    u'חמישי',
    u'שישי',
    u'שבת')
HEB_MONTH = (
    u'ינואר',
    u'פברואר',
    u'מרץ',
    u'אפריל',
    u'מאי',
    u'יוני',
    u'יולי',
    u'אוגוסט',
    u'ספטמבר',
    u'אוקטובר',
    u'נובמבר',
    u'דצמבר')
SCHOOL_TIME = (
    ('7:45', '8:30'),
    ('8:30', '9:15'),
    ('9:15', '10:00'),
    ('10:15', '11:00'),
    ('11:00', '11:45'),
    ('12:10', '12:55'),
    ('12:55', '13:40'),
    ('13:50', '14:35'),
    ('14:35', '15:20'),
    ('15:25', '16:10'),
    ('16:10', '16:55'),
    ('16:55', '17:40'),
    ('17:40', '18:25'))


def get_row(sheet, index, left_cut):
    row = sheet.iloc[index, left_cut:]
    lst = []
    is_empty = 1
    for i in row:
        if pd.isnull(i):
            i = ''
        else:
            is_empty = 0
        lst.append(i)
    html_entities = '<small style="color:#a1a4a5">{}</small><br><b>{}</b><br><small style="color:#a1a4a5">{}</small>'
    if index:
        index -= 1
        lst = [html_entities.format(SCHOOL_TIME[index][0], index, SCHOOL_TIME[index][1])] + lst
    if is_empty: return []
    return lst


def b(url, text):
    news = bs(rq.get(url).content, 'lxml').find('marquee')
    return [i for i in news.find_all('b') if text in i.text][0]


def to_table(url, up_cut, left_cut):
    sheet = pd.ExcelFile(url).parse(0)
    return [get_row(sheet, i, left_cut) for i in range(up_cut, len(sheet.index))]


def news_list(url):
    news = bs(rq.get(url).content, 'lxml').find('marquee')
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


def schedule_info(url=URL, text_to_find=TEXT_TO_FIND, default_info=DEFAULT_INFO, up_cut=UP_CUT, left_cut=LEFT_CUT):
    error = 0
    try:
        headline = b(url, text_to_find)
        title = headline.text.strip()
        day = title[-4:-2]
        month = '0' + title[-1]
        link = headline.find_next_sibling('a')['href'].strip()
        table = to_table(link, up_cut, left_cut)  # ONLINE: to_table(link) OFFLINE: to_table(local)
        date = headline.find_previous_sibling('sup').text[1:-1]
        date = date[:2] + u' ב' + HEB_MONTH[int(date[3:5])]
    except:
        title = 'אין מערכת'
        day = dt.date.today().strftime('%d')
        month = dt.date.today().strftime('%m')
        link = '#'
        table = []
        date = ''
        error = 1
    try:
        headline = b(url, text_to_find)
        description = headline.next_sibling.strip()
    except:
        description = default_info
    try:
        list = news_list(url)
    except:
        list = []
    weekday = dt.datetime.strptime(day + month + str(dt.datetime.now().year), '%d%m%Y').date().strftime('%w')
    time = u'יום ' + HEB_WEEKDAY[int(weekday)] + ', ' + day + u' ב' + HEB_MONTH[int(month) - 1]

    return {'headline_text': text_to_find, 'headline_link': link, 'url': url, 'title': title, 'info': description,
            'link': link,
            'time': time,
            'date': date, 'table': table,
            'error': error, 'news_list': list}
