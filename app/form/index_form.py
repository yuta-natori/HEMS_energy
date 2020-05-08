from django import forms

class TemperatureForm(forms.Form):
    tmpFile = forms.FileField()
    
class ElectricPowerForm(forms.Form):
    epFile = forms.FileField()
    
class HolidayForm(forms.Form):
    fromHoliday = forms.CharField()
    toHoliday = forms.CharField()