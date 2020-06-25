from django.shortcuts import render
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import datetime
from app.models.holiday_data import HolidayData
from app.models.temp_data import TempData
from app.models.electricity_data import ElectricityData
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from matplotlib.backends.backend_pdf import PdfPages
import img2pdf

#地域名のベクトル作成
region = '新横浜'

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic',
                               'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic',
                               'VL PGothic', 'Noto Sans CJK JP','Hiragino Kaku Gothic ProN']


def jyuyou_trend(request):
    if request.method == 'GET':
        return render(request, 'app/jyuyou_trend.html',{})

def execute_trend(request):
    if request.method == 'POST':
        os.getcwd()
        ##年間
        #クラス分け
        line_low = 5000
        line_high = 10000
        
        #分析したい年の入力
        s_date = '2017/01/01'
        e_date = '2018/11/30'
        
        #USER-ID指定
        user_id = 'snc.sh10000099'
        
        #ファイル選択
        
        #MySQL設定
        data_base = pd.DataFrame(list(ElectricityData.objects.filter(date__range=(s_date, e_date)).values()))
        data_base = data_base.sort_index()
        data_base_ymd = data_base['date'].str.split('/',expand = True)
        data_base_ymd.columns = ['year','month','day'] 
        
        #年　抽出
        data_base['year']=data_base_ymd['year']    #data_baseに追加
        #月　抽出
        data_base['month']=data_base_ymd['month'].astype(str)  #data_baseに追加
        
        
        #data = data_base.query("date >= '%s' & date <= '%s'"%(s_date,e_date))
        data_total= data_base[['date','hour','total']]
        data_class= data_base[['household_id','total']]
        
        #data_total = data.drop(['Unnamed: 0','user_id','minute','val1','val2','val3','val4','val5','val6','val7','val8','val9','val10','year','month'], axis = 1)
        #data_high = data.drop(['Unnamed: 0','date', 'hour','minute','val1','val2','val3','val4','val5','val6','val7','val8','val9','val10','year','month'], axis = 1)
        
        ##クラス分け
        #total
        total = data_total.groupby(['date', 'hour'], as_index=False).mean()
        total = total.sort_values(['date','hour'])
        total['date1'] = pd.to_datetime(total['date'])
        total = total.rename(columns={'total': 'x'}) #Rでxになっている為変更
        
        total_ = total[['date','hour','x']]
        total_['year'] = total_['date'].astype(str).str[:4]
        total_['month'] = total_['date'].astype(str).str[5:7]
        total_['day'] = total_['date'].astype(str).str[8:10]
        total_ = total_[['year','month','day','hour','x']]
        
        total_['year'] = total_['year'].astype(int)
        total_['month'] = total_['month'].astype(int)
        total_['day'] = total_['day'].astype(int)
        #total_.to_sql('demand_ele_hourly_%s_%s_%s'%(region_,s_date[:4]+s_date[5:7]+s_date[8:10],e_date[:4]+e_date[5:7]+e_date[8:10]), url, index=None,if_exists = 'replace')

        data_sum = data_class.groupby(('household_id'), as_index=False).sum()
        data_sum = data_sum.rename(columns={'total': 'x'})
        for row in data_sum.itertuples():
            totalFlg = checkClass(row[2], line_high, line_low)
            
        if totalFlg == 0:
            #high 
            high = data_sum.query('x > %s'%line_high)#値　ベタ打ち
            high = pd.merge(high,data_base,on = 'household_id')
            data_high = high[['date','hour','total']]
            high = data_high.groupby(['date','hour'], as_index=False).mean()
            high = high.sort_values(['date','hour'])
            high['date1'] =  pd.to_datetime(total['date'])
            high = high.rename(columns={'total': 'x'}) #Rでxになっている為変更
                        
            data_high = data_high[['date','hour','total']]
            data_high = data_high.groupby(['date'], as_index=True).agg({'total':['mean','max','min']}) 
            data_high = data_high.reset_index()
            data_high['year'] = data_high['date'].astype(str).str[:4]
            data_high['month'] = data_high['date'].astype(str).str[5:7]
            data_high['day'] = data_high['date'].astype(str).str[8:10]
            data_high = data_high[['year','month','day','total']]
            
            data_high['year'] = data_high['year'].astype(int)
            data_high['month'] = data_high['month'].astype(int)
            data_high['day'] = data_high['day'].astype(int)
        elif totalFlg == 1:
            #low
            low = data_sum.query('x < %s'%line_low)
            low = pd.merge(low,data_base,on = 'household_id')
            data_low = low[['date','hour','total']]
            low = data_low.groupby(['date','hour'],as_index=False).mean()
            low = low.sort_values(['date','hour'])
            low['date1'] = pd.to_datetime(total['date'])
            low = low.rename(columns={'total': 'x'}) #Rでxになっている為変更
                        
            data_low = data_low[['date','hour','total']]
            data_low = data_low.groupby(['date'], as_index=True).agg({'total':['mean','max','min']}) 
            data_low = data_low.reset_index()
            data_low['year'] = data_low['date'].astype(str).str[:4]
            data_low['month'] = data_low['date'].astype(str).str[5:7]
            data_low['day'] = data_low['date'].astype(str).str[8:10]
            data_low = data_low[['year','month','day','total']]
            
            data_low['year'] = data_low['year'].astype(int)
            data_low['month'] = data_low['month'].astype(int)
            data_low['day'] = data_low['day'].astype(int)
        else:    
            #middle
            mid = data_sum.query('%s <= x <= %s'%(line_low,line_high))#値　ベタ打ち R記載(x >= 10000 & x <= 20000) 
            mid = pd.merge(mid,data_base,on = 'household_id')
            data_mid = mid[['date','hour','total']]
            mid = data_mid.groupby(['date','hour'], as_index=False).mean()
            mid = mid.sort_values(['date','hour'])
            mid['date1'] = pd.to_datetime(total['date'])
            mid = mid.rename(columns={'total': 'x'}) #Rでxになっている為変更
                        
            data_mid = data_mid[['date','hour','total']]
            data_mid = data_mid.groupby(['date'], as_index=True).agg({'total':['mean','max','min']}) 
            data_mid = data_mid.reset_index()
            data_mid['year'] = data_mid['date'].astype(str).str[:4]
            data_mid['month'] = data_mid['date'].astype(str).str[5:7]
            data_mid['day'] = data_mid['date'].astype(str).str[8:10]
            data_mid = data_mid[['year','month','day','total']]
            
            data_mid['year'] = data_mid['year'].astype(int)
            data_mid['month'] = data_mid['month'].astype(int)
            data_mid['day'] = data_mid['day'].astype(int)
        
        #user毎の統計量
        user_all = data_base.query("household_id == '%s'"%user_id)
        user_all = user_all[['date','hour','total']]
        
        user_all = user_all[['date','hour','total']]
        user_all = user_all.groupby(['date'], as_index=True).agg({'total':['mean','max','min']}) 
        user_all = user_all.reset_index()
        user_all['year'] = user_all['date'].astype(str).str[:4]
        user_all['month'] = user_all['date'].astype(str).str[5:7]
        user_all['day'] = user_all['date'].astype(str).str[8:10]
        user_all = user_all[['year','month','day','total']]
        
        user_all['year'] = user_all['year'].astype(int)
        user_all['month'] = user_all['month'].astype(int)
        user_all['day'] = user_all['day'].astype(int)
        #user_all.to_sql('demand_ele_stats_%s_%s_%s_%s'%(region_,user_id[4:],s_date[:4]+s_date[5:7]+s_date[8:10],e_date[:4]+e_date[5:7]+e_date[8:10]), url, index=None,if_exists = 'replace')
        
        
        #地域名のベクトル作成
        region = '新横浜'
        y = str(data_base['year'])
        
        ##2017年　
        trend_year1(total,2017,'Total')
        year_fc_t_2017 = year_fc
        
        if totalFlg == 0:
            trend_year1(high,2017,'High')
        elif totalFlg == 1:
            trend_year1(low,2017,'Low')
        else:
            trend_year1(mid,2017,'Mid')
        
        #気温 読み込み
        temp_(2017)
        
        #年間電力需要量－外気温トレンド
        #画像取得
        distribution, histogram = trend_year2_glaph(year_fc_t_2017,year_fc,'blue','green','red',2017,totalFlg)
    
        '''TODO: 作成したFormに置き換える
        params = {
            'distribution' : "data:image/png;base64," + distribution,
            'histogram' : "data:image/png;base64," + histogram,
            'form' : DemandClassForm(request.POST or None)
            }
    
        #グラフをbase64形式で取得
        return render(request, 'app/jyuyou_trend.html', params)
        
        '''
        
        #月毎需要トレンド分析
        #trend_month(mid,2017,3,'Total')
        
        #週間需要トレンド分析
        #trend_week(total,2017,2,3,'Total')
        
        #24時間需要トレンド分析
        #trend_day(high,'High','2017/01/01')
        #trend_day(total,'Total','2017/02/13')
        
        """
        
        ##2018年
        trend_year1(total,2018,'Total')
        year_fc_t_2018 = year_fc
        
        #trend_year1(high,2018,'High')
        year_fc_h_2018 = year_fc
        
        #trend_year1(mid,2018,'Mid')
        year_fc_m_2018 = year_fc
        
        #trend_year1(low,2018,'Low')
        year_fc_l_2018 = year_fc
        
        
        #気温 読み込み
        temp_(2018)
        
        #年間電力需要量－外気温トレンド
        trend_year2_glaph(year_fc_t_2018,year_fc_h_2018,year_fc_m_2018,year_fc_l_2018,'blue','green','red',2018,totalFlg)
        
        #月毎需要トレンド分析
        trend_month(total,2018,3,'Total')
        
        #週間需要トレンド分析
        trend_week(low,2018,7,1,'High', name)
        
        #24時間需要トレンド分析
        trend_day(high,'High','2018/01/01')
        
        #2017年、2018年の結果を同時にグラフにしたもの
        #total
        glaph_(year_fc_t_2017,year_fc_t_2018,'black','blue','Total')
        print(year_fc_t_2017.describe())#基本統計量算出→「基本統計量の計算」のプログラムとして別に保存しますか？
        print(year_fc_t_2018.describe())
        
        #high
        
        glaph_(year_fc_h_2017,year_fc_h_2018,'black','blue','High')
        print(year_fc_h_2017.describe())
        print(year_fc_h_2018.describe())
        #mid
        glaph_(year_fc_m_2017,year_fc_m_2018,'black','blue','Mid')
        print(year_fc_m_2017.describe())
        print(year_fc_m_2018.describe())
        #low
        glaph_(year_fc_l_2017,year_fc_l_2018,'black','blue','Low')
        print(year_fc_l_2017.describe())
        print(year_fc_l_2018.describe())
        """
        
def checkClass(total,line_high,line_low):
    if total > line_high:
        return 0
    elif total < line_low:
        return 1
    else:
        return 2
        
def trend_year1(ds,y,cl_):
    global year_fc,min_max_df,month

    year_fc = ds
    year_fc_ymd = year_fc['date'].str.split('/',expand = True)
    year_fc_ymd.columns = ['year','month','day'] 


    #年　抽出
    year_fc['year']=year_fc_ymd['year'].astype(str)    #data_baseに追加
    #月　抽出
    year_fc['month']=year_fc_ymd['month'].astype(str)  #data_baseに追加


    min_max_df = year_fc[['x','year','month']]
    min_max_df = min_max_df.groupby(['year','month'],as_index=False).sum()


    global max
    max = np.max(min_max_df['x'],axis = 0) #グローバル変数として代入　defの中の場合、上の行に(global max)と書く
    global min
    min = np.min(min_max_df['x'],axis = 0) #グローバル変数として代入　defの中の場合、上の行に(global min)と書く


    year_fc = year_fc.query("year == '%s'"%y)
    year_fc = year_fc[['x','year','month']]
    year_fc = year_fc.groupby(['year','month'],as_index=False).sum()
   
    year_fc.to_csv("年間電力需要量トレンド(%s) %s年 %s.csv"%(cl_,y,region)) #class,year,regionベタ打ち



def trend_year2(ds,y):
    global year_fc,min_max_df,month

    year_fc = ds
    year_fc_ymd = year_fc['date'].str.split('/',expand = True)
    year_fc_ymd.columns = ['year','month','day'] 


    #年　抽出
    year_fc['year']=year_fc_ymd['year'].astype(str)    #data_baseに追加
    #月　抽出
    year_fc['month']=year_fc_ymd['month'].astype(str)  #data_baseに追加


    year_fc = year_fc.query("year == '%s'"%y)
    year_fc = year_fc[['x','year','month']]
    year_fc = year_fc.groupby(['year','month'],as_index=False).sum()
   
#外気温データ取得

def temp_(y):
    global temp,temp_ts 
    
    temperature = pd.DataFrame(list(TempData.objects.filter(date__contains=y).values()))
    temp = temperature['date'].str.split('/',expand = True)
    temp.columns = ['year','month','day']
    temp['x'] = temperature['temperature']
    
    #temperature = pd.read_sql_query("select * from shinyoko_temp where  year == '%s;"%y, cnt)
    #temp = temp.reset_index(drop=True) #index番号ふり直し
    #temp.columns = ['year','month','day','x'] #col名　変更 気温はｘにした
    temp = temp[['year','month','x']]
    temp['year'] = temp['year'].astype(np.float) #yearの型変換
    temp['month'] = temp['month'].astype(np.float) #monthの型変換
    temp['x'] = temp['x'].astype(np.float) #temperatureの型変換
    temp = temp.groupby(['year','month'],as_index=False).mean()
    temp_ts = list(temp['x'])
    
def trend_year2_glaph(cl_t,cl,col_h,col_m,col_l,y,totalFlg):
    global temp,temp_ts ,fig,month
    
    #目盛　内向き
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    month = list(range(1,len(cl_t['x'])+1)) #12だと11までしか出力されないので+1している
    if totalFlg == 0:
        plt.plot(month, cl['x'],c=col_h,label='需要家(High)')
    elif totalFlg == 1:
        plt.plot(month, cl['x'],c=col_l,label='需要家(Low)')
    else:
        plt.plot(month, cl['x'],c=col_m,label='需要家(Mid)')
    plt.xlim(1,len(cl_t['x']))
    plt.ylim(100,1700)
    plt.xticks(np.arange(1,len(cl_t['x'])+1,1))
    plt.yticks(np.arange(500,2500+1,500),rotation=90)

    plt.title('年間電力需要量－外気温トレンド(%s年)'%y,fontsize = 15) # タイトル　class,yearベタ打ち
    plt.xlabel('月(12ヵ月) \n 地域：%s'%region, fontsize = 13) # x軸ラベル　#サブタイトル
    plt.ylabel('電力需要量 (kWh)', fontsize = 13) # y軸ラベル
    plt.grid(False)
    plt.tick_params(labelsize=12) #x軸,y軸 目盛文字　サイズ 
    
    ax2 = ax1.twinx()
   
    plt.plot(month, temp['x'],c="black",linestyle="dashdot",label='外気温')
    plt.ylim(0,round(temp['x'].max())+5)
    plt.xticks(np.arange(1,len(cl_t['x'])+1,1))
    plt.yticks(np.arange(0,30+1,5),rotation=90)
    ax2.yaxis.tick_right()
    plt.ylabel('外気温 (℃)', fontsize = 13) # y軸ラベル
    ax2.yaxis.set_label_position("right") #軸ラベル　右側にする
    plt.grid(False)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2,fontsize=12, loc="upper left")
    plt.tick_params(labelsize=13) #x軸,y軸 目盛文字　サイズ

    plt.show()
    
    png_img,base64Img = makeImageBinary(fig)
    
    return base64Img



#月毎の消費電力
#year:年 month:月
#trend_month defの中
def trend_month(ds,y,m,cl_):
    global months,data_ts,day_bt,name,trendmonth
    
    months = ds
    month_ymd = months['date'].str.split('/',expand = True)
    month_ymd.columns = ['year','month','day'] 

    #年　抽出
    months['year']=month_ymd['year'].astype(str)
    #月　抽出
    months['month']=month_ymd['month'].astype(str)
    #日　抽出
    months['day']=month_ymd['day'].astype(str)
    
    months['year'] = months['year'].astype(np.int) #yearの型変換
    months['month'] = months['month'].astype(np.int) #monthの型変換
    months = months.query('year == %s & month == %s'%(y,m))
    months = months.groupby('date',as_index=False).sum()
    months = months[['date','x']]
    months['day'] = list(range(1,months['date'].count()+1))
    name = pd.DataFrame() #空のデータフレーム作成
    day_bt = [1,5,10,15,20,25,len(months.x)]
    data_ts = months['x']



    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    
    #棒グラフ　値指定
    plt.bar(months['day'],months['x'],ec='black')
    plt.xticks(day_bt,fontsize = 11)
    plt.xlim(0.6,months['x'].count()+0.4)
    plt.ylim(months['x'].min()-5,months['x'].max()+5)
    plt.yticks(fontsize = 11,rotation=90)
    
    plt.title('月毎電力需要量トレンド(%s) %s年%s月'%(cl_,y,m),fontsize = 15) # タイトル　class,yearベタ打ち
    plt.ylabel('電力需要量(kWh)', fontsize = 12) # y軸ラベル
    plt.xlabel('日 \n 地域：%s'%region, fontsize = 12) # x軸ラベル　#サブタイトル
    
    #上の枠線消す
    ax = plt.gca() 
    ax.spines["top"].set_color("none")
    
    plt.show()



#毎週の消費電力
def trend_week(ds,y,m,count,cl_):
    global pre_week,pre_week_ymd,pre_week1,pre_week2,ls,week,week_csv,x,week_t_24,week_glaph,mon,name
    pre_week = ds
    pre_week_ymd = pre_week['date'].str.split('/',expand = True)
    pre_week_ymd.columns = ['w_year','month','day']
    pre_week['w_year'] = pre_week_ymd['w_year'].astype(np.int) #yearの型変換
    pre_week = pre_week.query("year == '%s'"%y)
    pre_week['month'] = pre_week_ymd['month'].astype(np.int) #monthの型変換
    pre_week['day'] = pre_week_ymd['day'].astype(np.int) #dayの型変換
    pre_week['youbi'] = pre_week['date1'].dt.dayofweek #monday:0 sunday:6



    #第1週目から最終週まで番号を振る

    pre_week1 = pre_week.query("hour == '0' & youbi == '0'")  #月曜日の取得
    pre_week2 = pre_week.query("hour == '0' & day == '1'")    #月初の取得

    #上記二つのデータフレーム　縦結合
    pre_week1 = pd.concat([pre_week1, pre_week2])
    pre_week1 = pre_week1.sort_values(by='date')

    pre_week1=pre_week1.groupby('date',as_index=False).mean() #1日が月曜日の時の重複をなくしている

    #第何週であるかの変数(cnt)作成
    ls = []
    for i in list(range(1,12+1)):
        ls = list(ls + list(range(1,pre_week1.query("month == '%s'"%i)['month'].count()+1)))

    pre_week1['cnt'] = ls

    #元のデータフレームとマージ
    pre_week1 = pre_week1[['date','cnt']]
    pre_week = pd.merge(pre_week,pre_week1.astype(str),on = 'date',how="outer")
    pre_week['cnt'] = pre_week['cnt'].fillna(method='ffill')
    
    week = pre_week.query("month == '%s' & cnt == '%s'"%(m,count))

    if week['date'].nunique() < 7:
        if count == 1 and m >= 2:
            week = pre_week[(pre_week['date1']>=week['date1'].max()-datetime.timedelta(days=6)) 
                   & (pre_week['date1']<= week['date1'].max())]
        else:
            week = pre_week[(pre_week['date1']>=week['date1'].min()) 
                   & (pre_week['date1']<= week['date1'].min()+datetime.timedelta(days=6))]



    x = week['x']
    #week_t_24を作成するためにa,b作成　一行でできないか検討する
    a=np.array([1])
    b=([np.arange(24,24*week['date'].nunique()+1,24)])
    week_t_24 = np.append(a, b)

    week.loc[week['youbi'] == 0, 'week_youbi'] = "月"
    week.loc[week['youbi'] == 1, 'week_youbi'] = "火"
    week.loc[week['youbi'] == 2, 'week_youbi'] = "水"
    week.loc[week['youbi'] == 3, 'week_youbi'] = "木"
    week.loc[week['youbi'] == 4, 'week_youbi'] = "金"
    week.loc[week['youbi'] == 5, 'week_youbi'] = "土"
    week.loc[week['youbi'] == 6, 'week_youbi'] = "日"
    
    week_youbi = week['week_youbi'].unique()


    week['count'] = list(range(1,week['month'].count()+1))
    week_glaph = week[['x','count']]



    week_glaph.loc[week_glaph['count'] == 1, 'week_youbi'] = week_youbi[0]
    week_glaph.loc[week_glaph['count'] == 24, 'week_youbi'] = week_youbi[1]
    week_glaph.loc[week_glaph['count'] == 48, 'week_youbi'] = week_youbi[2]
    week_glaph.loc[week_glaph['count'] == 72, 'week_youbi'] = week_youbi[3]
    week_glaph.loc[week_glaph['count'] == 96, 'week_youbi'] = week_youbi[4]
    week_glaph.loc[week_glaph['count'] == 120, 'week_youbi'] = week_youbi[5]
    week_glaph.loc[week_glaph['count'] == 144, 'week_youbi'] = week_youbi[6]


    name = name.replace(np.nan,' ', regex=True)   #nanを空白にしてる
    
    #目盛　外向き
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'
    #棒グラフ　値指定
    week_len = len(week)
    plt.bar(np.arange(week_len),week_glaph['x'],ec='black')
    xlabels = name
    plt.xticks(range(0,len(week_glaph['week_youbi'])),xlabels,fontsize = 11)
    plt.xlim(0-0.5,week_glaph['x'].count()-0.5)
    plt.ylim(np.min(week['x']-0.1),np.max(week['x']+0.1))
    plt.yticks(fontsize = 11,rotation=90)
    xmin, xmax = 0,2.3
    plt.vlines([b], xmin, xmax, "black", linestyles='solid',linewidth = 1)
    ax = plt.gca() 
    ax.spines["top"].set_color("none")
    plt.tick_params(color='C0')   #軸目盛を表示させないために棒グラフと同じ色にしている

    plt.title('週間電力需要量トレンド(%s) %s年%s月%s日-%s月%s日'
              %(cl_,week['date'].min()[:4],week['date'].min()[5:7],week['date'].min()[8:10],
                      week['date'].max()[5:7],week['date'].max()[8:10]),fontsize = 15) # タイトル　class,yearベタ打ち
    
    plt.ylabel('電力需要量(kWh)', fontsize = 12) # y軸ラベル
    plt.xlabel('時間(7日分) \n 地域：%s'%region, fontsize = 12) # x軸ラベル　#サブタイトル
    plt.tick_params(color='white')      #軸目盛を表示させないために棒グラフと同じ色にしている
    plt.tick_params(axis='y', colors='black')

    plt.show()


#日付トレンド分析
#日付は指定される
#日毎トレンド分析_関数作成
def trend_day(ds,cl,ymd):
    global days,day_ymd,day_y,day_m,day_d,name,x,day_csv,trendday
    
    days = ds.query('date1 == "%s-%s-%s"'%(ymd[:4],ymd[5:7],ymd[8:10]))
    day_ymd = pre_week['date'].str.split('/',expand = True)
    day_ymd.columns = ['year','month','day'] 
    day_y = day_ymd['year'].astype(int) #yearを追加
    day_m = day_ymd['month'].astype(int) #monthを追加
    day_d = day_ymd['day'].astype(int) #dayを追加

    name = list(range(0,23))
    name_ = ["23時"]
    name.extend(name_)

    x = days['x']
    #names(x)=name

    #DBから読みこむプログラムに修正する必要あり
    trendday = pd.read_csv('日毎電力需要量トレンド(%s)_%s年%s月%s日 %s.csv'%(cl,ymd[:4],ymd[5:7],ymd[8:10],region))

    #目盛　外向き
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'in'
    #棒グラフ　値指定
    plt.bar(np.arange(len(x)),days['x'],ec='black')
    xlabels = name
    plt.xticks(range(0,len(days['x'])),xlabels,fontsize = 11)
    plt.xlim(0-0.4,days['x'].count()-0.5)
    plt.ylim(np.min(days['x'])-0.1,np.max(days['x'])+0.1)
    plt.yticks(fontsize = 11,rotation=90)     #y軸は自動取得にしている

    plt.title('日毎電力需要量トレンド (%s) %s年%s月%s日'%(cl,ymd[:4],ymd[5:7],ymd[8:10]),fontsize = 15) 
    plt.ylabel('電力需要量(kWh)', fontsize = 12) # y軸ラベル
    plt.xlabel('時間(24時間) \n 地域：%s'%region, fontsize = 12) # x軸ラベル　#サブタイトル
    
    #上と右の枠線消す
    ax = plt.gca() 
    ax.spines["top"].set_color("none")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_color("none")
    
    plt.tick_params(color='white')      #軸目盛を表示させないために棒グラフと同じ色にしている
    plt.tick_params(axis='y', colors='black')

    plt.show()
    
#年間比較グラフ
def glaph_(cl1,cl2,col1,col2,cl_):
    global fig,month,ls
    if len(cl1) != len(cl2):
        ls = abs(len(cl1) - len(cl2))
        if len(cl1) > len(cl2):
            cl2 = pd.DataFrame({"year":cl2['year'][0] ,
                                           "month": cl1['month'] ,
                                           "x": cl2['x'] })
        else:
            cl1 = pd.DataFrame({"year":cl1['year'][0] ,
                                           "month": cl2['month'] ,
                                           "x": cl1['x'] })

    #目盛　内向き
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'


    month = list(range(1,cl1['x'].count()+1)) #12だと11までしか出力されないので+1している
    plt.plot(month, cl1['x'],c=col1,linestyle="solid",label="%s"%cl1['year'][0])
    plt.plot(month, cl2['x'],c=col2,linestyle="dashed",label="%s"%cl2['year'][0])

    plt.xlim(1,cl1['x'].count())
    plt.xticks(np.arange(1,cl1['x'].count()+1,1))
    plt.yticks(rotation=90)

    plt.title('年間電力需要量トレンド分析(%s)'%cl_,fontsize = 15) # タイトル　class,yearベタ打ち
    plt.xlabel('月 \n 地域：%s'%region, fontsize = 12) # x軸ラベル　#サブタイトル
    plt.ylabel('電力需要量 (kWh)', fontsize = 12) # y軸ラベル
    plt.grid(False)
    plt.legend(fontsize=12) #凡例　サイズ
    plt.tick_params(labelsize=12) #x軸,y軸 目盛文字　サイズ

    #plt.show()
    
def makeImageBinary(fig):
    #作成したグラフをPNG形式に変換
    fig.canvas.draw()
    im = np.array(fig.canvas.renderer.buffer_rgba())
    img = Image.fromarray(im)
    
    #PNG画像をバイナリに変換
    buffer = BytesIO() 
    img.save(buffer, format="PNG")
    return img,base64.b64encode(buffer.getvalue()).decode().replace("'", "")