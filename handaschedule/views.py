# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from django.shortcuts import render
from django.utils import timezone

from .models import Post

URL = 'http://handasaim.co.il'
SUBTEXT = u'לוח'
UP_CUT = 3
LEFT_CUT = 3
DEFAULT_INFO = ''


def b(link):
    return [i for i in bs(requests.get(link).content, 'lxml').find('marquee').find_all('b') if SUBTEXT in i.text][0]


def to_table(url):
    xl = pd.ExcelFile(url)
    sheet = xl.parse(0)
    df = pd.read_excel(url, sheetname=0)
    return [sheet.iloc[i, LEFT_CUT:] for i in range(UP_CUT, len(df.index))]


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    title = b(URL).text.strip()
    try:
        info = b(URL).next_sibling.strip()
    except:
        info = DEFAULT_INFO
    link = b(URL).find_next_sibling('a')['href'].strip()
    time = b(URL).find_previous_sibling('sup').text[1:-1]
    try:
        table = to_table(link)
    except:
        table = []
    return render(request, 'handaschedule/post_list.html',
                  {'posts': posts, 'title': title, 'info': info, 'link': link, 'time': time, 'table': table})
