#！/usr/bin/env python
# -*- conding:utf-8 -*-
###########################################
#Time : 2020/7/7 14:13
#Author: Simon Chen
#File : Strage00637L.py
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
StockCodeDbName=DataBaseDir+'TwStock-No.db'
#if os.path.isfile(DateDataBaseName):
#    print("Date db exist")
#else:
#    print('%s exist' %(DateDataBaseName))

if os.path.isfile(StockCodeDbName):
    print("Code db exist")
else:
    print('%s not exist' %(StockCodeDbName))


StockCodeDb=sqlite3.connect(StockCodeDbName)
#Stock Code No
StockCode="00637L"
symbol = '00637L'
period = 600

# 设置基本参数
# type:绘制图形的类型，有candle, renko, ohlc, line等
# 此处选择candle,即K线图
# mav(moving average):均线类型,此处设置7,30,60日线
# volume:布尔类型，设置是否显示成交量，默认False
# title:设置标题
# y_label:设置纵轴主标题
# y_label_lower:设置成交量图一栏的标题
# figratio:设置图形纵横比
# figscale:设置图形尺寸(数值越大图像质量越高)
kwargs = dict(
    type='renko',
#    type='candle',
    mav=(5, 10, 20),
    volume=True,
    title='\n %s K chart' % (StockCode),
    ylabel='Price',
    ylabel_lower='Volume',
    figratio=(15, 10),
    figscale=5)


# 设置marketcolors
# up:设置K线线柱颜色，up意为收盘价大于等于开盘价
# down:与up相反，这样设置与国内K线颜色标准相符
# edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
# wick:灯芯(上下影线)颜色
# volume:成交量直方图的颜色
# inherit:是否继承，选填
mc = mpf.make_marketcolors(
    up='red',
    down='green',
    edge='i',
    wick='i',
    volume='in',
    inherit=True)

# 设置图形风格
# gridaxis:设置网格线位置
# gridstyle:设置网格线线型
# y_on_right:设置y轴位置是否在右
s = mpf.make_mpf_style(
    gridaxis='both',
    gridstyle='-.',
    y_on_right=False,
    marketcolors=mc)
# 设置均线颜色，配色表可见下图
# 建议设置较深的颜色且与红色、绿色形成对比
# 此处设置七条均线的颜色，也可应用默认设置
mpl.rcParams['axes.prop_cycle'] = cycler(
    color=['dodgerblue', 'deeppink',
    'navy', 'teal', 'maroon', 'darkorange',
    'indigo'])

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
mpl.rcParams['axes.unicode_minus']=False
# 设置线宽
mpl.rcParams['lines.linewidth'] = .5

'''
從資料庫讀取數據，並
1. 移除index這欄位
2. 把index設成‘Date'這欄位
3. 因為只想分析2019后的資料，所以把20190101前的資料拋棄
'''


#df = pd.read_sql('select * "2330"', conn, index_col=['stock_id'])
df=pd.read_sql(con=StockCodeDb,sql='SELECT * FROM '+'"'+StockCode+'"')
#移除index這欄位
df=df.iloc[:,1:]
df['Date']=pd.to_datetime(df['Date'])
df=df.set_index(['Date'])
df=df[df.index>'2019-01-01']
print(df)

#複製 數據
plot_df=df.copy()
plot_df=plot_df[['開盤價','最高價','最低價','收盤價','成交股數']]
#plot_df['datetime']=plot_df.index
plot_df['開盤價']=plot_df['開盤價'].apply(lambda x:x.replace(',',''))
plot_df['最高價']=plot_df['最高價'].apply(lambda x:x.replace(',',''))
plot_df['最低價']=plot_df['最低價'].apply(lambda x:x.replace(',',''))
plot_df['收盤價']=plot_df['收盤價'].apply(lambda x:x.replace(',',''))
plot_df['成交股數']=plot_df['成交股數'].apply(lambda x:x.replace(',',''))
plot_df['開盤價']=pd.to_numeric(plot_df['開盤價'])
plot_df['最高價']=pd.to_numeric(plot_df['最高價'])
plot_df['最低價']=pd.to_numeric(plot_df['最低價'])
plot_df['收盤價']=pd.to_numeric(plot_df['收盤價'])
plot_df['成交股數']=pd.to_numeric(plot_df['成交股數'])
#plot_df.columns=['open','high','low','close','Datetime']
plot_df.columns=['Open','High','Low','Close','Volume']


# 图形绘制
# show_nontrading:是否显示非交易日，默认False
# savefig:导出图片，填写文件名及后缀
mpf.plot(plot_df,
    **kwargs,
    style=s,
    show_nontrading=False)
'''

mpf.plot(plot_df, 
    **kwargs, 
    style=s, 
    show_nontrading=False,
    savefig='A_stock-%s %s_candle_line'
     % (symbol, period) + '.jpg')
'''
#plt.show()
print(df)
print(plot_df)
#mpf.plot(plot_df1,type='candle',mav=(5,10,15,20),volume=True)