# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render

from luz import *
from .forms import ClassPicker


def index(request):
    if request.method == 'POST':
        form = ClassPicker(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = ClassPicker()
    d = schedule_info().copy()
    d.update({'headline_link': 'luz', 'headline_text': 'לפי כיתה', 'headline_alt': 'מלאה',
              'main_margin': '0 auto -100px', 'main_height': '100%', 'form': form})
    return render(request, 'Schedule/index.html', d)


def luz(request):
    d = schedule_info().copy()
    d.update(
        {'headline_link': 'javascript:window.location = "/";', 'headline_text': 'מלאה', 'headline_alt': 'לפי כיתה',
         'main_margin': 'initial initial 0', 'main_height': 'auto'})
    return render(request, 'Schedule/luz.html', d)
