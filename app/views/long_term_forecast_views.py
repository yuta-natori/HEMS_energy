# -*- coding: utf-8 -*-
from django.shortcuts import render
import base64
from io import BytesIO
from PIL import Image

def long_term_forecast(request):
    
    #予測単位から取得する画像を選択
    img_name = 'long_term_forecast_in_month.png'
    
    #グラフ画像を取得
    png_img = Image.open('app/static/images/' + img_name)
    
    #24時間需要量予測日の指定がある場合はそのグラフも取得
    designeted_img = Image.open('app/static/images/long_term_forecast_24hours.png')
    designed = "data:image/png;base64," + makeImageBinary(designeted_img)

    params = {
        'graph' : "data:image/png;base64," + makeImageBinary(png_img),
        'designated' : designed
        #'form' : DemandClassForm(request.POST or None)
    }
    
    #グラフをbase64形式で取得
    return render(request, 'app/chouki_yosoku.html', params)


def makeImageBinary(img):
    #画像をバイナリに変換
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")