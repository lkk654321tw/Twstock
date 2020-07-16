#！/usr/bin/env python
# -*- conding:utf-8 -*-
##########################################
#Time : 2020/7/10 15:54
#Author: Simon Chen
#File : StrageRenko.py
###########################################




import os
import platform
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import time
import datetime
import mplfinance as mpf
from cycler import cycler# 用于定制线条颜色
import matplotlib as mpl# 用于设置曲线参数
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.dates import DateFormatter
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker

###########################################
# define function
###########################################
def trans_datetime(date_time):
    return ''.join(str(date_time).split(' ')[0].split('-'))


#设定工作目录
if platform.system()== "Windows":
    print(platform.system())
    WorkDir = os.getcwd() + "\\..\\Data-twse\\"
    DataBaseDir = WorkDir + 'DataBase\\'
else:
    print(platform.system())
    WorkDir = os.getcwd() + "/../Data-twse/"
    DataBaseDir = WorkDir + 'DataBase/'

print("WorkDir="+WorkDir)
print("DataBaseDir="+DataBaseDir)
DateDataBaseName = DataBaseDir + 'TwStock-Date.db'
StockCodeDbName  = DataBaseDir+'TwStock-No.db'
if os.path.isfile(DateDataBaseName):
    print("Date db %s exist" %DateDataBaseName)
else:
    print('%s exist' %(DateDataBaseName))

if os.path.isfile(StockCodeDbName):
    print("Code db %s exist" %StockCodeDbName)
else:
    print('%s not exist' %(StockCodeDbName))

DateDb=sqlite3.connect(DateDataBaseName)
CodeDb=sqlite3.connect(StockCodeDbName)

#從資料庫讀回表單
#df = pd.read_sql('select * "2330"', DateDb, index_col=['stock_id'])
#df = pd.read_sql(con=DateDb,sql='SELECT * FROM '+ '"'+date+'"')
#select * from sqlite_master where type=’index’ and name=‘索引名’;

table_name = pd.read_sql(con=DateDb, sql='SELECT * FROM sqlite_master')


#begin_date = table_name.iloc[0].tbl_name
#begin_date="20040212"
begin_date="20200101"
# 轉換日期
begin_date = datetime.date(int(begin_date[0:4]), int(begin_date[4:6]), int(begin_date[6:8]))
print("begin date=")
print(begin_date)
#end_date = table_name.iloc[-1].tbl_name
end_date = "2020706"
end_date = datetime.date(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:8]))
print("end date=")
print(end_date)



now_date=begin_date
#end_date = begin_date + + datetime.timedelta(days=20)
total_df= pd.DataFrame()
i=0;
while now_date < end_date:
    now_date = table_name.iloc[i*2].tbl_name
    now_date = datetime.date(int(now_date[0:4]), int(now_date[4:6]), int(now_date[6:8]))
#    if((i%10) == 0):
    print("i=%d" % i)
    print(now_date)
    date=trans_datetime(now_date)
    i=i+1
    df=pd.read_sql(con=DateDb,sql='SELECT * FROM '+ '"'+date+'"')
    df['Date']=now_date
    total_df=total_df.append(df)

print("i=%d" %i)
print(now_date)
print("df=")
print(df)
print("total_df=")
print(total_df)
