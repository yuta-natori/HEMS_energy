# -*- coding: utf-8 -*-
from django.shortcuts import render
import numpy as np
from matplotlib import rcParams
#↓グラフ表示するために追加したライブラリ
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64
#form
from app.form.demand_class_form import DemandClassForm
#model
from app.models.electricity_data import ElectricityData

def analysis_demand_class(request):    
 
    # グラフ描画処理
    def class_glaph(year, query_data):
        global data_sum,count
        
        #data_sum= year.groupby(['user_id'],as_index=False).sum()
        #data_sum = data_sum[['user_id','total']]
    
        #data_sum = data_sum.dropna(axis = 0) #欠損　除去
    
            #変数の数　count作成
        count = list(range(1,query_data.count()+1))
        #data_sum['count'] = count #countを追加

        global fig,plot
        #年間
        #目盛　内向き
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
    
        #散布図　値指定
        fig=plt.figure(figsize = (7, 5)) #fig=　pdf出力のため
        plot=plt.scatter(count, query_data.values_list('total'),s = 20)
    
        #タイトル　ラベル
        plt.title('%s年　需要家別電力需要量分布(年間)'%year,fontsize = 15) # タイトル
        plt.xlabel('需要家番号 \n 地域：%s'%region, fontsize = 12) # x軸ラベル　#サブタイトル
        plt.ylabel('電力需要量(kWh)', fontsize = 12) # y軸ラベル
        plt.grid(False) # (8)目盛線の表示
    
        #軸目盛　間隔　
        plt.xlim(0,len(count))
        plt.xticks(fontsize = 11)
        plt.ylim(0, max(query_data.values_list('total', flat=True))+1000)
        plt.yticks(np.arange(0, max(query_data.values_list('total', flat=True))+1000, 2500),fontsize = 11,rotation=90)
        plt.tick_params(length = 3) #仮
    
        #クラス分け　ライン(横)
        #ライン設定時のみ適用
        if line_low is not None and line_high is not None:
            xmin, xmax = 0,len(count)
            plt.hlines([line_low], xmin, xmax, '#e41a1c', linestyles='solid',linewidth = 1.5) 
            plt.hlines([line_high], xmin, xmax, '#e41a1c', linestyles='solid',linewidth = 1.5)
            plt.text(len(count)-5,line_low+100, "%s"%line_low,size = 11, color = "#e41a1c")
            plt.text(len(count)-6,line_high+100, "%s"%line_high,size = 11, color = "#e41a1c")
        
        #作成したグラフをPNG形式に変換
        fig.canvas.draw()
        im = np.array(fig.canvas.renderer.buffer_rgba())
        img = Image.fromarray(im)
        
        #PNG画像をバイナリに変換
        buffer = BytesIO() 
        img.save(buffer, format="PNG")
        base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")

        #年間
        #目盛　外向き
        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'
        
        #ヒストグラム　値指定
        fig_ = plt.figure(figsize=(7, 6))
        plot = plt.hist(query_data.values_list('total', flat=True),bins=16,range=(0, 16000),ec='black')
        
        #タイトル　ラベル
        plt.title('電力需要量―需要家ヒストグラム%s年'%year,fontsize = 15) # タイトル
        plt.xlabel('年間電力需要量 (kWh)\n 地域：%s'%region, fontsize = 12) # x軸ラベル　#サブタイトル
        plt.ylabel('需要家数', fontsize = 12) # y軸ラベル
        plt.grid(False) # (8)目盛線の表示
    
        #軸目盛　間隔
        plt.xticks(fontsize = 11)
        plt.yticks(list(range(0,20+1,2)),fontsize = 11,rotation=90)
        plt.xlim(0,16000)
        plt.ylim(0,20)
        
        #上と右の枠線消す
        ax = plt.gca() 
        ax.spines["top"].set_color("none")
        ax.spines["right"].set_color("none")
        
        #クラス分け　ライン(縦)
        #ライン設定時のみ適用
        if line_low is not None and line_high is not None:
            ymin, ymax = 0,20
            plt.vlines([line_low], ymin, ymax, '#e41a1c', linestyles='solid',linewidth = 1.5) 
            plt.vlines([line_high], ymin, ymax, '#e41a1c', linestyles='solid',linewidth = 1.5)
        
        fig_.canvas.draw()
        im_ = np.array(fig_.canvas.renderer.buffer_rgba())
        img_ = Image.fromarray(im_)
        
        #PNG画像をバイナリに変換
        buffer_ = BytesIO() 
        img_.save(buffer_, format="PNG")
        base64Img_ = base64.b64encode(buffer_.getvalue()).decode().replace("'", "")

        return base64Img, base64Img_
    
    #日本語　フォント
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic',
                                   'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic',
                                   'VL PGothic', 'Noto Sans CJK JP','Hiragino Kaku Gothic ProN']

    #期間指定
    select_year = request.POST['year']
    
    #分析したい年の入力
    s_date = select_year + '/01/01'
    e_date = select_year + '/12/31'
    
    #分析時期判定
    select_season = request.POST['season']
    line_low = None
    line_high = None
    
    if select_season == 'year':
        line_low, line_high = setLineHighLow(
            request.POST['year_min_line'], 
            request.POST['year_max_line'])
        
    elif select_season == 'summer':
        line_low, line_high = setLineHighLow(
            request.POST['summer_min_line'],
            request.POST['summer_max_line'])
        
        s_date = select_year + '/06/01'
        e_date = select_year + '/08/31'
    elif select_season == 'winter':
        line_low, line_high = setLineHighLow(
            request.POST['winter_min_line'],
            request.POST['winter_max_line'])
        
        s_date = select_year + '/12/01'
        e_date = str(int(select_year) + 1) + '/02/28' #TODO: うるう年の判定
        
    #地域名
    #region_= 'shinyoko' #TODO: 地域名から地域ID的なものを取得
    area = request.POST['area']
    
    #読み込みファイル指定　既存のもの
    #data_base = pd.read_sql_query("SELECT user_id, date, hour, minute, total from %s_data where date between '%s' and '%s'"%(region_,s_date,e_date),cnt)
    data_base = ElectricityData.objects.filter(
        date__range = (s_date, e_date),
        area = area
    )
    print("data_base-------------------------↓")
    print(data_base)
    print(data_base.values())
    print(data_base.values_list('total', flat=True).first() )
    print(data_base.count())
    
    #年　抽出
    #data_base['year']=data_base['date'].astype(str).str[:4]    #data_baseに追加 
    #月　抽出
    #data_base['month']=data_base['date'].astype(str).str[5:7]  #data_baseに追加

    
    #年の要素数　地域名
    #data_year = data_base.date.astype(str).str[:4]
    region = '新横浜'

    #画像取得
    distribution, histogram = class_glaph(select_year, data_base)
    
    params = {
        'distribution' : "data:image/png;base64," + distribution,
        'histogram' : "data:image/png;base64," + histogram,
        'form' : DemandClassForm(request.POST or None)
    }
    
    #グラフをbase64形式で取得
    return render(request, 'app/jyuyou_class.html', params)

def setLineHighLow(min_line, max_line):
    line_low = None
    line_high = None
    
    if min_line and max_line :
        line_low = int(min_line)
        line_high = int(max_line)
    
    return line_low, line_high