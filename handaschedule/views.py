from django.shortcuts import render
from .models import Post
from django.utils import timezone
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from django.http import HttpResponse
from openpyxl import load_workbook

def get_webpage(url):
	return requests.get(url)

def get_links(response):
	soup = bs(response.content,'lxml')
	marquee = soup.find('marquee')
	links = marquee.find_all('a')
	return links

def open_file(file_url):
    data = file_url
    xl = pd.ExcelFile(data)
    sheet1 = xl.parse(0)
    column = sheet1.iloc[:,2].real
    df = pd.read_excel(data, sheetname=0)
    return [sheet1.iloc[:,i].real[3:] for i in range(len(df.columns))]

def cool():
    response = get_webpage('http://handasaim.co.il/')
    #response = json.load(response)['return']
    links= get_links(response)
    url=links[0].get('href').strip()
    c = open_file(url)
    return c

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'handaschedule/post_list.html', {'posts': posts, 'lis': cool()})