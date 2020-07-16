#！/usr/bin/env python
# -*- conding:utf-8 -*-
###########################################
#Time : 2020/7/6 14:39
#Author: Simon Chen
#File : DownloadStockData.py
###########################################


import requests
import pandas as pd
import io
import datetime
import time
import os
import sqlite3
import glob
import platform

def crawler (date_time):
    #盤後資訊=>每日收盤行情=>全部（不含權證）
    url='https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+date_time+'&type=ALLBUT0999'
    print(url)
    #用 requests的get把資料讀進來
    page = requests.get(url)
    #用字串的splitlines，分成一行行
    use_text = page.text.splitlines()
    #用for loop 找出起始點行號
    for i,text in enumerate(use_text):
        if text== '"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",':
            initial_point =i
            break
    #在每行結尾加上"\n"
    test_df=pd.read_csv(io.StringIO(''.join([text[:-1] + "\n" for text in use_text[initial_point:]])))
    # 把證券代號欄位的“及=去掉
    test_df['證券代號']=test_df['證券代號'].apply(lambda x:x.replace('"',''))
    test_df['證券代號']=test_df['證券代號'].apply(lambda x:x.replace('=',''))
#    print(test_df.head())
    return test_df

def trans_datetime(date_time):
    return ''.join(str(date_time).split(' ')[0].split('-'))

if platform.system()== "Windows":
    print(platform.system())
    WorkDir=os.getcwd()+"\\..\\Data-twse\\"
    CsvDir=WorkDir+'csv\\'
    DateDataBaseName=WorkDir+'DataBase\\'+'TwStock-Date.db'
    StockNoDbName=WorkDir+'DataBase\\'+'TwStock-No.db'
else:
    print(platform.system())
    WorkDir=os.getcwd()+"/../Data-twse/"
    CsvDir=WorkDir+'csv/'
    DateDataBaseName=WorkDir+'DataBase/'+'TwStock-Date.db'
    StockNoDbName=WorkDir+'DataBase/'+'TwStock-No.db'

db1=sqlite3.connect(DateDataBaseName)
StockNoDb=sqlite3.connect(StockNoDbName)
print(WorkDir)
if os.path.isfile(DateDataBaseName):
    print("Date db exist")
else:
    print('%s not exist' %(DateDataBaseName))

if os.path.isfile(StockNoDbName):
    print("Code db exist")
else:
    print('%s not exist' %(StockNoDbName))

all_csv_file=glob.glob(CsvDir+'*.csv')

# 讀取資料庫內的資料表
table_name = pd.read_sql(con=db1, sql='SELECT * FROM sqlite_master')
# 取得資料庫最後日期
begin_date = table_name.iloc[-1].tbl_name
# 轉換日期
begin_date = datetime.date(int(begin_date[0:4]), int(begin_date[4:6]), int(begin_date[6:8]))
# 取得今天日期
end_date = datetime.date.today()
# end_date= begin_date + datetime.timedelta(days=7)
print('begin_date:')
print(begin_date)
print('end_date:')
print(end_date)

df_dict={}
now_date = begin_date
while now_date < end_date:
    time.sleep(1)
    now_date = now_date + datetime.timedelta(days=1)
    # monady=0 sunday=6
    print(now_date.weekday())
    if now_date.weekday() <=4:
        try:
            key = trans_datetime(now_date)
            csv_name = CsvDir + key + '.csv'
            print(csv_name)
            if os.path.isfile(csv_name):
                print("%s is exist" %(csv_name))
            else:
                df=crawler(trans_datetime(now_date))
                print('Success !!!' + ' '+trans_datetime(now_date))
#               df_dict.update({trans_datetime(now_date):df})
                df_dict.update({key:df})
                df_dict[key].to_csv(csv_name)
        except:
            print('Fail at' + ' '+trans_datetime(now_date))


