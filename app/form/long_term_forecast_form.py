# -*- coding: utf-8 -*-
from django import forms
from django.views import generic

CHOICE_UNIT = (
    (None, "-"),
    ("month", "月"),
    ("day", "日"),
    ("hour", "時")    
)

class LongTermForecastForm(forms.Form):
    area = forms.CharField(
        max_length=50,
        required=True,
    )
    
    fromForecast = forms.CharField(
        max_length=10,
        required=True,
    )
    
    toForecast = forms.CharField(
        max_length=10,
        required=True,
    )
    
    forecastUnit = forms.ChoiceField(
        required=True,
        choices=CHOICE_UNIT,
    )
    
    forecastDate = forms.CharField(
        max_length=10,
        required=False,
    )
    
    forecastTemp = forms.CharField(
        required=False,
    )