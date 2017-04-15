# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

page = 'http://handasaim.co.il'
title = u'לוח'


def get_webpage(url):
    return requests.get(url)


def get_links(response):
    soup = bs(response.content, 'lxml')
    marquee = soup.find('marquee')
    links = marquee.find_all('a')
    return links


def open_file(file_url):
    data = file_url
    xl = pd.ExcelFile(data)
    sheet1 = xl.parse(0)
    column = sheet1.iloc[:, 2].real
    df = pd.read_excel(data, sheetname=0)
    return [sheet1.iloc[:, i].real[3:] for i in range(len(df.columns))]


def get_sheet_url(page):
    response = get_webpage(page)
    links = get_links(response)
    print links[0].get('href').strip()


def mega(page):
    response = get_webpage(page)
    links = get_links(response)
    link = links[0]
    print \
        [i for i in bs(response.content, 'lxml').find('marquee').find_all('b') if title in i.text][0].parent.find_all(
            'a')[
            0]['href']


mega(page)
