# -*- coding: utf-8 -*-
from django import forms
from django.views import generic

CHOICE_SEASONS = (
    (None, "-"),
    ("year", "年間分析"),
    ("summer", "夏季分析（6月～8月）"),
    ("winter", "冬季分析（12月～2月）")    
)

CHOICE_YEARS = (
    (2014, 2014),
    (2015, 2015),
    (1999, 1999),
    (2000, 2000)
)

class DemandClassForm(forms.Form):
    area = forms.CharField(
        label='地域の指定',
        max_length=50,
        required=True,
    )
    
    year = forms.ChoiceField(
        label='予測開始年月日年の選択',
        choices=CHOICE_YEARS,
    )
    
    season = forms.ChoiceField(
        label='分析時期の選択',
        choices=CHOICE_SEASONS,
        required=False,
        widget=forms.Select(attrs = {'onchange' : "chkselect();"})
    )
    
    year_max_line = forms.IntegerField(
        label='年間ライン上限値の指定',
        required=False,
    )
    
    year_min_line = forms.IntegerField(
        label='年間ライン下限値の指定',
        required=False,
    )
    
    summer_max_line = forms.IntegerField(
        label='夏季ライン上限値の指定',
        required=False,
    )
    
    summer_min_line = forms.IntegerField(
        label='夏季ライン下限値の指定',
        required=False,
    )
    
    winter_max_line = forms.IntegerField(
        label='冬季ライン上限値の指定',
        required=False,
    )
    
    winter_min_line = forms.IntegerField(
        label='冬季ライン下限値の指定',
        required=False,
    )