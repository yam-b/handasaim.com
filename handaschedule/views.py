# -*- coding: utf-8 -*-
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from django.shortcuts import render
from django.utils import timezone

from untitled.settings import BASE_DIR
from .models import Post

URL = 'http://handasaim.co.il'
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


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    title = b(URL).text.strip()
    try:
        info = b(URL).next_sibling.strip()
    except:
        info = DEFAULT_INFO
    link = b(URL).find_next_sibling('a')['href'].strip()
    time = b(URL).find_previous_sibling('sup').text[1:-1]
    local = os.path.join(BASE_DIR, 'handaschedule/schedule.xlsx')
    table = to_table(local)  # or to_table(local)
    return render(request, 'handaschedule/post_list.html',
                  {'posts': posts, 'title': title, 'info': info, 'link': link, 'time': time, 'table': table})
