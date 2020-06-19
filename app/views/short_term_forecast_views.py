# -*- coding: utf-8 -*-
from django.shortcuts import render
import base64
from io import BytesIO
from PIL import Image

def short_term_forecast(request):
    
    #グラフ画像を取得
    png_img = Image.open('app/static/images/short_term_forecast.png')
    
    params = {
        'graph' : "data:image/png;base64," + makeImageBinary(png_img)
        #'form' : DemandClassForm(request.POST or None)
    }
    
    #グラフをbase64形式で取得
    return render(request, 'app/tanki_yosoku.html', params)


def makeImageBinary(img):
    #画像をバイナリに変換
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode().replace("'", "")