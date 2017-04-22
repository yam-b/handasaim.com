# coding=utf-8
from django import forms

from luz import *


class ClassPicker(forms.Form):
    table = schedule_info()['table']
    tup = tuple((i, item) for i, item in enumerate(table[0]))
    my_options = forms.ChoiceField(label=u'כיתה', choices=tup, widget=forms.Select(attrs={'class': 'selectpicker',
                                                                                          'data-style': 'btn-default',
                                                                                          'data-width': 'auto',
                                                                                          'data-size': '5',
                                                                                          'style': 'display:none'}))
