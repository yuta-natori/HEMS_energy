# -*- coding: utf-8 -*-
from django import forms
from django.views import generic

CHOICE_DATAS = (
    (None, "-"),
    (1, "DBデータから選択1"),
    (2, "DBデータから選択2"),
    (3, "DBデータから選択3"),
    (4, "DBデータから選択4")
)

CHOICE_SEASONS = (
    (None, "-"),
    ("year", "年間分析"),
    ("summer", "夏季分析（6月～8月）"),
    ("winter", "冬季分析（12月～2月）")    
)

class DemandClassForm(forms.Form):
    data = forms.ChoiceField(
        widget=forms.Select, 
        choices=CHOICE_DATAS, 
        label='使用データの指定',
        required=True,
    )

    area = forms.CharField(
        label='地域の指定',
        max_length=50,
        required=True,
    )
    
    year = forms.ChoiceField(
        label='予測開始年月日年の選択',
        choices=CHOICE_DATAS,
    )
    
    season = forms.ChoiceField(
        label='分析時期の選択',
        choices=CHOICE_SEASONS,
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