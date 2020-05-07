from django.shortcuts import render
import sqlalchemy as sqa 
import jpholiday
import numpy as np
from datetime import datetime
from datetime import timedelta
import pandas as pd
import mysql.connector
import os

def index(request):
    if request.method == 'GET':
    	return  render(request,'app/index.html',{})  
	
def holiday(request):
    if request.method == 'POST':
        def daterange(date1,date2):    
            for n in range(int((date2 - date1).days)+1):
                yield date1 + timedelta(n)
        
        holidayFrom = request.POST.get('from')
        holidayTo = request.POST.get('to')
        start_date = datetime.strptime(holidayFrom, '%Y/%m/%d').date()
        end_date   = datetime.strptime(holidayTo, '%Y/%m/%d').date()
        
        #evens[]リスト作成 
        evens = [] 
        #(2014,1,1~2018,12,31)の期間でループする 
        for dt in daterange(start_date, end_date):    
            date = dt.strftime("%Y/%m/%d")                         #日付    
            if not date == np.nan:                        
                hoho = jpholiday.is_holiday(dt)                   #祝日判定 T or F                
                if not hoho == np.nan:                                                      
                    hyo = dt.weekday()                            # 曜日を取得            
                    if not hyo == np.nan:                                
                        if hyo == 5 or hyo == 6 or hoho == True:      #土日と 祝日に1の値を入れる                    
                            hois = 1                                              
                        else:                    
                            hois = 0                                                        
                        day = date[5:10]                           #三が日に1 の値を入れる 
                        if day == "01/01" or day == "01/02" or day == "01/03":                    
                            hois = 1                    
                            evens.append([date,hoho,hyo,hois,day])                
                        else:                    
                            hois = hois                    
                            evens.append([date,hoho,hyo,hois,day])                    
        #evens[]リストをデータフレームに変換                    
        holiday = pd.DataFrame(evens,columns = ['date','holiday','youbi','is_holiday','day'])                    
        holiday = holiday[['date','is_holiday']]            
             
        
        #sql書き込み
        cnt = mysql.connector.connect(
              host='192.168.56.1', # 接続先
              port='3306',
              user='user', # mysqlのuser
              password='pass', # mysqlのpassword
              database='hems_data_shinyoko',
              charset='utf8' ,
              auth_plugin='mysql_native_password'
              )
        cnt.cursor()
        
        # カーソル取得
        cnt.cursor(buffered=True)    
        url = 'mysql://user:pass@192.168.56.1/hems_data_shinyoko?charset=utf8'
        sqa.create_engine(url, echo=True)
        
        holiday.to_sql('holiday', url, index=None,if_exists = 'replace')  
        return render(request,'app/index.html',{})
def temperature(request):
    
    if request.method == 'POST':
        temperatureFile = request.POST.get('data_create')
    
        cnt = mysql.connector.connect(
          host='192.168.56.1', # 接続先
          port='3306',
          user='user', # mysqlのuser
          password='pass', # mysqlのpassword
          database='hems_data_shinyoko',
          charset='utf8',
          auth_plugin='mysql_native_password'
          )
        
        #カーソル取得
        cnt.cursor(buffered=True)
        url = 'mysql://user:pass@192.168.56.1/hems_data_shinyoko?charset=utf8'
        sqa.create_engine(url, echo=True)
        
        os.chdir("C:\\Users\\ClientAdmin\\Desktop\\Downloads")
         
        temp = pd.read_csv(temperatureFile, engine='python')
        temp = temp.drop([0,1,2,3], axis=0) #必要のない行削除
        temp = temp.reset_index(drop=True) #index番号ふり直し
        temp.columns = ['year','month','day','temperature','',''] #col名　変更 気温はｘにした
        temp = temp[['year','month','day','temperature']]
        temp['temperature'] = temp['temperature'].astype('float64')
        temp['year']= temp['year'].astype(int)
        temp['month']= temp['month'].astype(int)
        temp['day']= temp['day'].astype(int)
        
        temp['date'] = temp['year'].astype(str)+'/'+temp['month'].astype(str)+'/'+temp['day'].astype(str)
        temp['date'] = pd.to_datetime(temp['date'])
        temp['date'] = temp['date'].dt.strftime("%Y/%m/%d")
        temp.to_sql('shinyoko_temp', url, index=None,if_exists = 'append')
        
        return render(request,'app/index.html',{})
def electric_power(request):
    
    if request.method == 'POST':
        
        electricFile = request.POST.get('data_create')
    
        ##Path指定
        os.chdir("C:\\Users\\ClientAdmin\\Desktop\\受領\\受領\\HEMS_Analysis_demo")
    
        ##地域指定
        region = 'shinyoko'
        #def main():
            # MySQL接続
        cnt = mysql.connector.connect(
              host='192.168.56.1', # 接続先
              port='3306',
              user='user', # mysqlのuser
              password='pass', # mysqlのpassword
              database='hems_data_shinyoko',
              charset='utf8',
              auth_plugin='mysql_native_password'
              )
        
        # カーソル取得
        cnt.cursor(buffered=True)
            
        url = 'mysql://user:pass@192.168.56.1/hems_data_shinyoko?charset=utf8'
        sqa.create_engine(url, echo=True)
        data = pd.read_csv(electricFile) 
        data.to_sql('%s_data'%region, url, index=None,if_exists = 'replace')

        return render(request,'app/index.html',{})

def toukei_keisan(request):
    # 対応するhtmlファイルを指定
    return render(request,'app/toukei_keisan.html',{})
    
def jyuyou_class(request):
	return render(request, 'app/jyuyou_class.html',{})
    
def jyuyou_trend(request):
	return render(request, 'app/jyuyou_trend.html',{})

def jyuyou_modeling(request):
	return render(request, 'app/jyuyou_modeling.html',{})

def chouki_yosoku(request):
	return render(request, 'app/chouki_yosoku.html',{})	

def tanki_yosoku(request):
	return render(request, 'app/tanki_yosoku.html',{})
	
	

# Create your views here.
