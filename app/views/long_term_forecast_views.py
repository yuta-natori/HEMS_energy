# -*- coding: utf-8 -*-
from django.shortcuts import render
import base64
from io import BytesIO
from PIL import Image
#form
from app.form.long_term_forecast_form import LongTermForecastForm

def long_term_forecast(request):
    
    #予測単位から取得する画像を選択
    unit = request.POST['forecastUnit']
    img_name = None
    
    if unit == 'month':
        img_name = 'long_term_forecast_in_month.png'
    elif unit == 'day':
        img_name = 'long_term_forecast_in_day.png'
    elif unit == 'hour':
        img_name = 'long_term_forecast_in_hour.png'
    
    
    #グラフ画像を取得
    png_img = Image.open('app/static/images/' + img_name)
    
    #24時間需要量予測日の指定がある場合はそのグラフも取得 
    if request.POST['forecastDate']:    
        designated_img = Image.open('app/static/images/long_term_forecast_24hours.png')
        designated = "data:image/png;base64," + makeImageBinary(designated_img)
    else:
        designated = None

    params = {
        'graph' : "data:image/png;base64," + makeImageBinary(png_img),
        'designated' : designated,
        'form' : LongTermForecastForm(request.POST or None)
    }
    
    #グラフをbase64形式で取得
    return render(request, 'app/chouki_yosoku.html', params)


def makeImageBinary(img):
    #画像をバイナリに変換
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")