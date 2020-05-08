# -*- coding: utf-8 -*-
from django.shortcuts import render
import numpy as np
from matplotlib import rcParams
import pandas as pd
import mysql.connector
#↓グラフ表示するために追加したライブラリ
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64
#form
from app.demand_class_form import DemandClassForm

def analysis_demand_class(request):    
 
    # グラフ描画処理
    def class_glaph(y):
        global data_year,data_sum,count
        #年間
        data_year = data_base.query("year == '%s'"%y) #年　抽出
    
        data_sum= data_year.groupby(['user_id'],as_index=False).sum()
        data_sum = data_sum[['user_id','total']]
    
        data_sum = data_sum.dropna(axis = 0) #欠損　除去
    
            #変数の数　count作成
        count = list(range(1,data_sum['total'].count()+1))
        data_sum['count'] = count #countを追加
            
        global fig,plot
        
        #fig = plt.figure(figsize = (6, 5))
        #ax = plt.subplot(2,1,1)
        #ax.set_position([0.2,0.64,0.7,0.3])
        #年間
        #目盛　内向き
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
    
        #散布図　値指定
        fig=plt.figure(figsize = (7, 5)) #fig=　pdf出力のため
        plot=plt.scatter(data_sum['count'], data_sum['total'],s = 20)
    
        #タイトル　ラベル
        plt.title('%s年　需要家別電力需要量分布(年間)'%y,fontsize = 15) # タイトル
        plt.xlabel('需要家番号 \n 地域：%s'%region, fontsize = 12) # x軸ラベル　#サブタイトル
        plt.ylabel('電力需要量(kWh)', fontsize = 12) # y軸ラベル
        plt.grid(False) # (8)目盛線の表示
    
        #軸目盛　間隔　
        plt.xlim(0,data_sum['count'].count())
        plt.xticks(fontsize = 11)
        plt.ylim(0, data_sum['total'].max()+1000)
        plt.yticks(np.arange(0, data_sum['total'].max()+1000, 2500),fontsize = 11,rotation=90)
        plt.tick_params(length = 3) #仮
    
        #クラス分け　ライン(横)
        xmin, xmax = 0,data_sum['count'].count()
        plt.hlines([line_low], xmin, xmax, '#e41a1c', linestyles='solid',linewidth = 1.5) 
        plt.hlines([line_high], xmin, xmax, '#e41a1c', linestyles='solid',linewidth = 1.5)
        plt.text(data_sum['count'].count()-5,line_low+100, "%s"%line_low,size = 11, color = "#e41a1c")
        plt.text(data_sum['count'].count()-6,line_high+100, "%s"%line_high,size = 11, color = "#e41a1c")
        #fig.savefig("%s年　需要家別電力需要量分布(年間).png"%y)
        
        #作成したグラフをPNG形式に変換
        fig.canvas.draw()
        im = np.array(fig.canvas.renderer.buffer_rgba())
        img = Image.fromarray(im)
        
        #PNG画像をバイナリに変換
        buffer = BytesIO() 
        img.save(buffer, format="PNG")
        base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    
        #ax_ = plt.subplot(2,1,2)
        #ax_.set_position([0.2,0.13,0.7,0.3])
        #年間
        #目盛　外向き
        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'
        
        #ヒストグラム　値指定
        fig_ = plt.figure(figsize=(7, 6))
        plot = plt.hist(data_sum['total'],bins=16,range=(0, 16000),ec='black')
        
        #タイトル　ラベル
        plt.title('電力需要量―需要家ヒストグラム%s年'%y,fontsize = 15) # タイトル
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
        ymin, ymax = 0,20
        plt.vlines([line_low], ymin, ymax, '#e41a1c', linestyles='solid',linewidth = 1.5) 
        plt.vlines([line_high], ymin, ymax, '#e41a1c', linestyles='solid',linewidth = 1.5)
        
        #fig_.savefig("電力需要量―需要家ヒストグラム%s年.png"%y)
        
        fig_.canvas.draw()
        im_ = np.array(fig_.canvas.renderer.buffer_rgba())
        img_ = Image.fromarray(im_)
        
        #PNG画像をバイナリに変換
        buffer_ = BytesIO() 
        img_.save(buffer_, format="PNG")
        base64Img_ = base64.b64encode(buffer_.getvalue()).decode().replace("'", "")
        
        print(base64Img)
        print(base64Img_)
        return base64Img, base64Img_
    
    #日本語　フォント
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic',
                                   'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic',
                                   'VL PGothic', 'Noto Sans CJK JP','Hiragino Kaku Gothic ProN']
    #MySQL設定
    cnt = mysql.connector.connect(
              host='192.168.11.8', # 接続先
              port='3306',
              user='user', # mysqlのuser
              password='pass', # mysqlのpassword
              database='hems_data_shinyoko',
              charset='utf8',
              auth_plugin='mysql_native_password'
              )
    
    #期間指定
    date1_base = '2015-01-01'
    date2_base = '2015-12-31'
    
    #分析したい年の入力
    s_date = '2015/01/01'
    e_date = '2015/12/31'
    
    #地域名
    region_= 'shinyoko'
    
    #読み込みファイル指定　既存のもの
    data_base = pd.read_sql_query("SELECT user_id, date, hour, minute, total from %s_data where date between '%s' and '%s'"%(region_,s_date,e_date),cnt)
    #data_base = pd.read_csv('shinyoko(20140803-20181130).csv')
    data_base = data_base.sort_index()
    #年　抽出
    data_base['year']=data_base['date'].astype(str).str[:4]    #data_baseに追加 
    #月　抽出
    data_base['month']=data_base['date'].astype(str).str[5:7]  #data_baseに追加
    data_base['date1'] = pd.to_datetime(data_base['date'])
    #CSV　出力
    data_base.to_csv('data_%s-%s.csv'%(date1_base,date2_base),index=False)
    
    #年の要素数　地域名
    data_year = data_base['date'].astype(str).str[:4]
    region = '新横浜'
    
    ##年間
    #クラス分け
    line_low = 5000
    line_high = 10000
    
    #画像取得
    distribution, histogram = class_glaph(2015)
    
    params = {
        'distribution' : "data:image/png;base64," + distribution,
        'histogram' : "data:image/png;base64," + histogram,
        'form' : DemandClassForm(request.POST or None)
    }
    
    #グラフをbase64形式で取得
    return render(request, 'app/jyuyou_class.html', params)