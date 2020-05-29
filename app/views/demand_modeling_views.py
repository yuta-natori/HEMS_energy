# -*- coding: utf-8 -*-
from django.shortcuts import render
import os 
#os.chdir("C:\\Users\\ClientAdmin\\Desktop\\test")      #フォイルを作成したい場所を指定
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import rcParams
from sklearn.linear_model import LinearRegression
#↓グラフ表示するために追加したライブラリ
from PIL import Image
from io import BytesIO
import base64
#form
from app.form.demand_modeling_form import DemandModelingForm
#model
from app.models.holiday_data import HolidayData
from app.models.electricity_data import ElectricityData
from app.models.temp_data import TempData
from app.models.holiday_coefficient import HolidayCoefficient
from app.models.energy_data_after_screening import EnergyDataAfterScreening
from app.models.power_demand_profile import PowerDemandProfile
from app.models.temperature_variation_coefficient import TemperatureVariationCoefficient

def demand_modeling(request) : 
    os.chdir("C:\\Users\\ClientAdmin\\Desktop\\test")      #フォイルを作成したい場所を指定
    region = request.POST['area']   #ファイル名に指定している地域名
    #sql書き込み

    url = 'mysql+pymysql://user:pass@192.168.11.8/hems_data_shinyoko?charset=utf8'
    
    # サンプルデータを読み込む 
    data_base = pd.DataFrame(list(ElectricityData.objects.all().values()))
    data_base = data_base.sort_index()
    data_base['year'] = data_base['date'].astype(str).str[:4]
    data_base['month'] = data_base['date'].astype(str).str[5:7]
    
    #期間指定
    date1_base = request.POST['fromScreening']
    date2_base = request.POST['toScreening']
    
    data_base['date1'] = pd.to_datetime(data_base['date'])
    data = data_base.query("date1 >= '%s' & date1 <= '%s'"%(date1_base,date2_base))
    data['date'] = data['date'].astype(str).str[:4]+'/'+data['date'].astype(str).str[5:7]+'/'+data['date'].astype(str).str[8:10]
      
    holiday = pd.DataFrame(list(HolidayData.objects.all().values()))
    #csv出力 
    holiday.to_csv("holiday.csv", index=True)      
    
    
    ####データスクリーニング#### 
    #異常値、欠損値を除外したデータを作成 
    #異常値は年間総消費電力が10000kWh以上のものとする 
    #各ユーザ日ごとに集計（欠損データがある日は除外） 
    #欠損値件数算出 
    #電力消費量の欠損値合計数 
    remove_1 = data_base.total.isnull().sum() 
    
    #カテゴリわけしてグループ集計 
    #各ユーザー日毎の1時間平均算出 
    user_daily = data_base.groupby(['household_id','date']).agg({'total':'mean'}) 
    
    #列ラベル変更
    user_daily = user_daily.rename(columns = {'total':'hourly_mean'}) 
    
    #各ユーザー日毎の1日平均算出 
    user_daily['daily_total'] = user_daily['hourly_mean']*24
    user_daily=user_daily.reset_index()
    #休日変動係数 
    holiday = pd.read_csv('holiday.csv') 
    
    #前後合わせて３週間を含む移動平均 
    daily = user_daily.groupby(['date']).agg({'daily_total':'mean'}) 
    
    window = 21 
    daily["moving_average"] = daily["daily_total"].rolling(window).mean() 
    
    daily['normalized'] = daily["daily_total"]/daily["moving_average"] 
    
    
    #休日情報をマージ 
    daily = pd.merge(daily, holiday, on = 'date',how = 'outer') 
    #休日変動係数ヒストグラム描画 
    
    daily_hei=daily.query('is_holiday == 0')['normalized'] 
    daily_kyu=daily.query('is_holiday == 1')['normalized'] 
    
    daily_ = daily.dropna(subset=['daily_total'], how='all') 
     #日本語フォント 
    rcParams['font.family'] = 'sans-serif' 
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao',        
                                    'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP'] 
        
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'
    
    fig = plt.figure(figsize = (7,5)) 
    plt.xticks([0,0.5,1.0,1.5,2.0],fontsize = 12)
    plt.yticks(fontsize = 12,rotation=90) 
    
    
    plt.ylim(-0.3,10)
    plt.xlim(0,2)
    plt.title('休日変動係数ヒストグラム',fontsize = 14) 
    plt.xlabel('電力需要量/3週間移動平均(休日変動係数)',fontsize = 12) 
    plt.ylabel('電力需要密度(需要家数)',fontsize = 12)
     
    ax = plt.gca() 
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")
    
    # ヒストグラムを描画する 
    plt.hist(daily_hei, range = (0, 2),bins = 1000,color = '#ff00ff40',ec = '#ff00ff',alpha = 0.4,density = 'T',label='平日'); 
    plt.hist(daily_kyu, range = (0, 2),bins = 1000,color = '#0000ff40',ec = '#0000ff',alpha = 0.4,density = 'T',label='休日'); 
    
                    
    #平均値追加 
    plt.vlines(np.mean(daily_hei), ymin = -0.3, ymax = 10, linestyle = 'solid',colors = 'r', linewidth = 3,label='平日平均') 
    plt.vlines(np.mean(daily_kyu), ymin = -0.3, ymax = 10, linestyle = 'solid',colors = 'b', linewidth = 3,label='休日平均') 
    plt.legend()
    plt.text(1.5,10.05, 
             "(%s.%s-%s.%sデータ)"%(daily_.date.min()[:4],daily_.date.min()[5:7],
                               daily_.date.max()[:4],daily_.date.max()[5:7]),size = 9,color='black')

    #グラフをバイナリ変換
    histogram_img = makeImageBinary(fig)
    
    #月ごとの日次変動係数を求める 
    data_base_umh= pd.DataFrame({"year": data_base['date'].astype(str).str[:4],
                             "month": data_base['date'].astype(str).str[5:7],
                             "day": data_base['date'].astype(str).str[8:10]})
    
    
    user_month_hour_ = data_base[['household_id','total','hour']]
    
    #連結 
    user_month_hour = pd.concat([user_month_hour_,data_base_umh], axis=1)
    
    #除去件数 
    remove_2 = user_month_hour.query('total >= 10') 
    user_month_hour = user_month_hour.query('total < 10')
    user_month_hour['month'] = user_month_hour['month'].astype(int)  #月を数値に変換
    
    #日時係数データ洗替
    PowerDemandProfile.objects.all().delete()
    
    profile_imgs = []
    for i in range(12):
        profile_imgs.append("data:image/png;base64," + daily_demand(i+1, region, url, user_month_hour))
    
    #気温データ読み込み
    temperature = pd.DataFrame(list(TempData.objects.filter(
        date__range = (date1_base, date2_base)
        ).values()))
    temperature['date1'] = pd.to_datetime(temperature['date'])
    temperature = temperature[['date','temperature','date1']]
    
    #data2に休日データ，気温データを結合する
    user_daily_with_temp = pd.merge(user_daily,holiday,on='date')
    user_daily_with_temp = pd.merge(user_daily_with_temp,temperature,on='date')
    
    #休日補正係数の結合
    ls_nml = [[daily_hei.mean(),daily_kyu.mean()]]
    holiday_coef=pd.DataFrame(ls_nml, index=['holiday_coef'], columns=['0','1'])
    holiday_coef = holiday_coef.T #行列入れ替え
    holiday_coef = holiday_coef.reset_index()
    holiday_coef = holiday_coef.rename(columns={'index': 'is_holiday'})
    holiday_coef = holiday_coef.astype(float)
    
    #休日係数登録
    holiday_coef_data = [] 
    for row in holiday_coef.itertuples():
        holiday_coef_data.append(HolidayCoefficient(
            is_holiday=row[1],
            holiday_coef=row[2]))
        
    HolidayCoefficient.objects.all().delete()
    HolidayCoefficient.objects.bulk_create(holiday_coef_data)
    
    user_daily_with_temp = pd.merge(user_daily_with_temp,holiday_coef, on = 'is_holiday')
    
    #休日補正→日の一時間毎の平均消費電量に休日係数をかけた(normalizedはその日のトータル消費で電力に近い)
    user_daily_with_temp['normalized'] = user_daily_with_temp['hourly_mean']/user_daily_with_temp['holiday_coef']*24 
    
    #ユーザーごとの平均値→ユーザー毎の元データの範囲(今回は一年間)の休日補正済みの平均消費電力
    user_daily_average_normalized = user_daily_with_temp.groupby(['household_id'], as_index=False).agg({'normalized':'mean'})
    
    #平均値の結合
    user_daily_with_temp = pd.merge(user_daily_with_temp,user_daily_average_normalized,on = 'household_id')
    
    #ノーマライズ→日の一時間毎の休日係数をかけた平均消費電量をユーザーごとの休日係数でかけた平均消費電量で割った 間違っているかも...
    user_daily_with_temp['normalized2'] = user_daily_with_temp['normalized_x']/user_daily_with_temp['normalized_y']
    
    #ノーマライズ上限・下限値を取得
    upper_limit = request.POST['normalizeMax']
    lower_limit = request.POST['normalizeMin']
    
    #フィルター→0<normalized2<5だけど　0<narmalized2<3 でもいいかもしれない
    user_daily_with_temp_filtered = user_daily_with_temp.query("normalized2 > " + lower_limit + " & normalized2 < " + upper_limit)
    
    #フィルタで除去された件数
    remove_3 = user_daily_with_temp.query("normalized2 <= " + lower_limit + " or normalized2 > " + upper_limit)
    
    #日ごとに平均
    daily_with_temp = user_daily_with_temp_filtered.groupby(['date'],as_index=False).agg({'normalized2':'mean'})
    daily_with_temp = pd.merge(daily_with_temp,temperature,on = 'date')
    daily_with_temp['temperature'] = daily_with_temp['temperature'].astype(float)
    
    normarized_img = modering(region, url, daily_with_temp)

    #スクリーニングしたデータをcsvに出力
    #スクリーニングしたデータフレームを作成
    data_scr = user_daily_with_temp_filtered[['household_id','date']] #列指定
    data_scr = data_scr.drop_duplicates()                        #重複削除
    data_scr = pd.merge(data_scr,data.query("total<10"),on=('household_id','date'))  #クラス別分析で作成されたdata
    data_scr = data_scr.sort_values(['date', 'hour','household_id'])
    #data_scr = data_scr.iloc[:, 0:15]
    
    
    #除去件数の算出
    remove_2['date'] = remove_2['year']+'/'+remove_2['month']+'/'+remove_2['day']
    remove_23 = pd.merge(remove_2,remove_3,on=('household_id','date'),how='outer')
    remove = remove_1 + len(remove_23['household_id'])
    #↓3行足した　実行してない
    data_scr['remove']  = np.nan
    data_scr['remove'][0] = remove
    data_scr['remove'] = data_scr['remove'].replace(np.nan,' ', regex=True)
    """
    energy_data = [] 
    for row in data_scr.itertuples():
        energy_data.append(EnergyDataAfterScreening(
            id=row[3],
            household_id=row[1],
            date=pd.to_datetime(row[2]).strftime("%Y/%m/%d"),
            hour=row[3],
            minute=row[4],
            total=row[5],
            val1=row[6],
            val2=row[7],
            val3=row[8],
            val4=row[9],
            val5=row[10],
            val6=row[11],
            val7=row[12],
            val8=row[13],
            val9=row[14],
            val10=row[15]))
    """
    EnergyDataAfterScreening.objects.all().delete()
    regist_data = data_scr.drop(['id', 'area', 'year', 'month', 'date1', 'remove'], axis=1)
    
    energy_data = [] 
    for row in regist_data.itertuples():
        energy_data.append(EnergyDataAfterScreening(
            id=row[3],
            household_id=row[1],
            date=pd.to_datetime(row[2]).strftime("%Y/%m/%d"),
            hour=row[3],
            minute=row[4],
            total=row[5],
            val1=row[6],
            val2=row[7],
            val3=row[8],
            val4=row[9],
            val5=row[10],
            val6=row[11],
            val7=row[12],
            val8=row[13],
            val9=row[14],
            val10=row[15]))
        
    EnergyDataAfterScreening.objects.bulk_create(energy_data)
    #regist_data.to_sql('t_energy_data_after_screening', url, index=None,if_exists = 'replace')
    
    params = {
        'histogram' : "data:image/png;base64," + histogram_img,
        'profiles' : profile_imgs,
        'normarized' : "data:image/png;base64," + normarized_img,
        'form' : DemandModelingForm(request.POST or None)
    }
    
    return render(request, 'app/jyuyou_modeling.html', params)


#各月の時間ごとの日時係数算出 
def daily_demand(month, region, url, user_month_hour):
    global umh,tmp
    
    fig = plt.figure(figsize = (7,5)) 
    
    umh = user_month_hour.query("month == '%s'"%month) 
    tmp = umh.groupby(['month','hour'],as_index=False).agg({'total':'mean'})    
    tmp['rate'] = tmp.total/sum(tmp.total)        
    
    plt.ylim(-0.005,0.105) 
    plt.xlabel("時間 \n 地域:%s"%region,fontsize = 12) 
    plt.ylabel("需要率",fontsize = 12) 
    plt.title("電力需要プロファイル (%s月)"%month,fontsize = 14)

    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12,rotation=90) 

    plt.plot(tmp['hour'], tmp['rate'], linewidth=1, color="black")
    
    power_demand_profile_data = [] 
    for row in tmp.itertuples():
        power_demand_profile_data.append(PowerDemandProfile(
            month=row[1],
            hour=row[2],
            total=row[3],
            rate=row[4]))
    
    PowerDemandProfile.objects.bulk_create(power_demand_profile_data)

    return makeImageBinary(fig)


##気温需要モデリングプロット
def modering(region, url, daily_with_temp):
    global lm_w,lm_c,average_no_aircon
    #登録用リスト
    temp_coefficient_data = []     
    fig = plt.figure(figsize = (7,5)) 
    
    #散布図　値指定
    plt.scatter(daily_with_temp['temperature'], daily_with_temp['normalized2'],c='white',ec = 'black', s=20, marker='o')

    #タイトル　ラベル
    plt.title('日平均外気温―日電力需要量',fontsize = 14) # タイトル
    plt.xlabel('日平均外気温(℃) \n 地域：'+region, fontsize = 12) # x軸ラベル　#サブタイトル \n 地域：'+region
    plt.ylabel('日毎電力需要量(ノーマライズ値)', fontsize = 12) # y軸ラベル

    #軸目盛　間隔　
    plt.xlim(daily_with_temp['temperature'].min()-1,daily_with_temp['temperature'].max()+1)
    plt.xticks(np.arange(0,daily_with_temp['temperature'].max(),5),fontsize = 12)
    plt.yticks(fontsize = 12,rotation=90)
    plt.tick_params(length = 3) 
    

    #線形回帰　暖房
    
    lr = LinearRegression()
    daily_with_temp.lm_w = daily_with_temp.query("temperature < 15")
    X = daily_with_temp.lm_w[['temperature']].values         # 説明変数（Numpyの配列）
    Y = daily_with_temp.lm_w['normalized2'].values         # 目的変数（Numpyの配列）
    
    lr.fit(X,Y)                         # 線形モデルの重みを学習
    
    lm_w = pd.DataFrame({
        'status': [1], 
        'intercept': [lr.intercept_], 
        'coefficient': [lr.coef_[0]]})
    
    temp_coefficient_data.append(TemperatureVariationCoefficient(
            status=1,
            coefficient=lr.intercept_,
            intercept=lr.coef_[0]))
    
    #回帰直線
    plt.plot(X, lr.predict(X) , color = 'darkblue',linewidth = 1)
    #線形回帰　冷房
    daily_with_temp.lm_c = daily_with_temp.query("temperature > 23")
    X = daily_with_temp.lm_c[['temperature']].values         # 説明変数（Numpyの配列）
    Y = daily_with_temp.lm_c['normalized2'].values         # 目的変数（Numpyの配列）
        
    lr.fit(X,Y)                         # 線形モデルの重みを学習

    lm_c = pd.DataFrame({
        'status': [2], 
        'intercept': [lr.intercept_], 
        'coefficient': [lr.coef_[0]]})
    
    temp_coefficient_data.append(TemperatureVariationCoefficient(
            status=2,
            coefficient=lr.intercept_,
            intercept=lr.coef_[0]))

    #回帰直線
    plt.plot(X, lr.predict(X), color = 'red',linewidth = 1)
    #冷暖房ない区間の平均
    average_no_aircon = daily_with_temp.query("temperature >15 & temperature < 23").mean()     #.mean()の前に['normalized2']を指定すれば必要なものだけに出来る
    average_no_aircon = average_no_aircon.drop('temperature', axis=0)
    xmin, xmax = daily_with_temp['temperature'].min()-1,daily_with_temp['temperature'].max()+1
    plt.hlines(average_no_aircon['normalized2'], xmin, xmax, 'lime', linestyles='solid',linewidth = 1.25) 
    plt.text(np.max(X)-8,np.max(daily_with_temp['normalized2'])+0.06, 
             "(%s.%s-%s.%sデータ)"%(daily_with_temp.date.min()[:4],daily_with_temp.date.min()[5:7],
                                   daily_with_temp.date.max()[:4],daily_with_temp.date.max()[5:7]),size = 10,color='black')

    temp_coefficient_data.append(TemperatureVariationCoefficient(
            status=0,
            coefficient=average_no_aircon['normalized2']))   
        
    #期間表示
    TemperatureVariationCoefficient.objects.all().delete()
    TemperatureVariationCoefficient.objects.bulk_create(temp_coefficient_data)
    
    return makeImageBinary(fig)
    
def makeImageBinary(fig):
    #作成したグラフをPNG形式に変換
    fig.canvas.draw()
    im = np.array(fig.canvas.renderer.buffer_rgba())
    img = Image.fromarray(im)
    
    #PNG画像をバイナリに変換
    buffer = BytesIO() 
    img.save(buffer, format="PNG")
    return  base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    