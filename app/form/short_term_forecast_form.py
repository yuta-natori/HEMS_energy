# -*- coding: utf-8 -*-
from django import forms
from django.views import generic

class ShortTermForecastForm(forms.Form):
    area = forms.CharField(
        max_length=50,
        required=True,
    )
    
    startForecast = forms.CharField(
        max_length=10,
        required=True,
    )
    
    forecastTime = forms.CharField(
        required=False,
    )