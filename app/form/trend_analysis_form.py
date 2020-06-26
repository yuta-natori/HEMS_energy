# -*- coding: utf-8 -*-
from django import forms

CHOICE_YEARS = (
    (None, "-"),
    (1998, 1998),
    (1999, 1999),
    (2000, 2000),
    (2001, 2001),
    (2002, 2002),
    (2003, 2003),
    (2004, 2004),
    (2005, 2005),
    (2006, 2006),
    (2007, 2007),
    (2008, 2008),
    (2009, 2009),
    (2010, 2010),
    (2011, 2011),
    (2012, 2012),
    (2013, 2013),
    (2014, 2014),
    (2015, 2015),
    (2016, 2016),
    (2017, 2017),
    (2018, 2018),
    (2019, 2019),
    (2020, 2020)
)

CHOICE_MONTH = (
    (None, "-"),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12)
)

CHOICE_WEEK = (
    (None, "-"),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4)
)

CHOICE_DISPLAY = (
    ("daily", "日毎トレンド分析"),
    ("weekly", "週刊トレンド分析"),
    ("monthly", "月間トレンド分析"),
    ("yearly", "年間トレンド分析"),
    ("temp", "外気温需要トレンド分析")
)

class TrendAnalysisFormClass(forms.Form):
    area = forms.CharField(
        max_length=50,
        required=True,
    )
    
    fromYear = forms.ChoiceField(
        choices=CHOICE_YEARS,
    )
    
    toYear = forms.ChoiceField(
        choices=CHOICE_YEARS
    )
    
    dailyTrend = forms.CharField(
        max_length=10,
        required=False,
    )
    
    weeklyYear = forms.ChoiceField(
        choices=CHOICE_YEARS,
        required=False,
    )
    
    weeklyMonth = forms.ChoiceField(
        choices=CHOICE_MONTH,
        required=False,
    )
    
    weeklyWeek = forms.ChoiceField(
        choices=CHOICE_WEEK,
        required=False,
    )
    
    yearlyYear = forms.ChoiceField(
        choices=CHOICE_YEARS,
        required=False,
    )
    
    yearlyMonth = forms.ChoiceField(
        choices=CHOICE_MONTH,
        required=False,
    )
    
    maxLine = forms.IntegerField(
        required=False,
    )
    
    minLine = forms.IntegerField(
        required=False,
    )
    
    trendDisplay = forms.MultipleChoiceField(
        required=True,
        initial=["daily"],
        widget=forms.RadioSelect,
        choices=CHOICE_DISPLAY,
    )