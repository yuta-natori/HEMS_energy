# -*- coding: utf-8 -*-
from django import forms
from django.views import generic

class DemandModelingForm(forms.Form):
    area = forms.CharField(
        max_length=50,
        required=True,
    )
    
    fromScreening = forms.CharField(
        max_length=10,
        required=True,
    )
    
    toScreening = forms.CharField(
        max_length=10,
        required=True,
    )
    
    excValue = forms.IntegerField(
        required=False,
    )
    
    normalizeMax = forms.IntegerField(
        required=False,
    )
    
    normalizeMin = forms.IntegerField(
        required=False,
    )