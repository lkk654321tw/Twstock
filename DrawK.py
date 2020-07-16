#！/usr/bin/env python
# -*- conding:utf-8 -*-
###########################################
#Time : 2020/7/16 16:50
#Author: Simon Chen
#File : DrawK.py
###########################################

###########################################
###########################################
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

###########################################
###########################################
# 從DataBase 讀入資料
WorkDir = "D:\\stock\\Data-twse\\"
DataBaseDir = WorkDir + 'DataBase\\'
StockCodeDbName = DataBaseDir + 'TwStock-No.db'
StockCodeDb = sqlite3.connect(StockCodeDbName)
# 台積電股票代碼
StockCode = "2330"
'''
從資料庫讀取數據，並
1. 移除index這欄位
2. 把index設成‘Date'這欄位
3. 因為只想分析2019后的資料，所以把20190101前的資料拋棄
'''

# df = pd.read_sql('select * "2330"', conn, index_col=['stock_id'])
df = pd.read_sql(con=StockCodeDb, sql='SELECT * FROM ' + '"' + StockCode + '"')
# 移除index這欄位
df = df.iloc[:, 1:]
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index(['Date'])
df = df[df.index > '2019-09-01']

# 複製 數據
plot_df = df.copy()
plot_df = plot_df[['開盤價', '最高價', '最低價', '收盤價', '成交股數']]
# plot_df['datetime']=plot_df.index
plot_df['開盤價'] = plot_df['開盤價'].apply(lambda x: x.replace(',', ''))
plot_df['最高價'] = plot_df['最高價'].apply(lambda x: x.replace(',', ''))
plot_df['最低價'] = plot_df['最低價'].apply(lambda x: x.replace(',', ''))
plot_df['收盤價'] = plot_df['收盤價'].apply(lambda x: x.replace(',', ''))
plot_df['成交股數'] = plot_df['成交股數'].apply(lambda x: x.replace(',', ''))
plot_df['開盤價'] = pd.to_numeric(plot_df['開盤價'])
plot_df['最高價'] = pd.to_numeric(plot_df['最高價'])
plot_df['最低價'] = pd.to_numeric(plot_df['最低價'])
plot_df['收盤價'] = pd.to_numeric(plot_df['收盤價'])
plot_df['成交股數'] = pd.to_numeric(plot_df['成交股數'])
# plot_df.columns=['open','high','low','close','Datetime']
plot_df.columns = ['open', 'high', 'low', 'close', 'volume']


# 計算"收盤價"移動平均副函數 MA
# data:資料表
# perioas：多少天的MA
def moving_average(data, periods):
    return data['close'].rolling(periods).mean()


# 計算KD值
''' 
1. 計算RSV：（今日的收盤價-最近9天的最低價）/(最近9天的最高價-最近9天的最低價)
2. 計算K值：K=2/3*(昨天的K值)+1/3(今日RSV)
3. 計算D值：D=2/3*(昨天的D值)+1/3(今日K值)
'''


def KD(data):
    # step 1 計算RSV
    copy_df = data.copy()
    copy_df['min'] = copy_df['low'].rolling(9).min()
    copy_df['max'] = copy_df['high'].rolling(9).max()
    copy_df['RSV'] = (copy_df['close'] - copy_df['min']) / (copy_df['max'] - copy_df['min'])

    # step 2 計算K值
    # 去除 NaN 欄位
    copy_df = copy_df.dropna()
    k_list = [50]
    for index, rsv in enumerate(list(copy_df['RSV'])):
        k_yesterday = k_list[index]
        k_today = 2.0 / 3.0 * (k_yesterday) + 1 / 3.0 * rsv
        k_list.append(k_today)

    # 從1開始第一個數值50是填補進去的
    copy_df['K'] = k_list[1:]

    # step 3 計算D值
    d_list = [50]
    for index, k in enumerate(list(copy_df['K'])):
        d_yesterday = d_list[index]
        d_today = 2 / 3 * d_yesterday + 1 / 3 * k
        d_list.append(d_today)

    copy_df['D'] = d_list[1:]
    use_df = pd.merge(data, copy_df[['K', 'D']], left_index=True, right_index=True, how='left')
    # print(copy_df)
    return use_df


plot_df = plot_df.reset_index()
# plot_df['Date']=mdates.date2num(plot_df['Date'])

data_plot = KD(plot_df)
data_plot.reset_index()
data_plot['Date'] = data_plot.index

# 畫K線圖
ma5 = moving_average(data_plot, 5)
ma10 = moving_average(data_plot, 10)
ma20 = moving_average(data_plot, 20)
length = len(data_plot['Date'].values[20:])
figure = plt.figure(facecolor='white', figsize=(15, 10))
date_tickers = plot_df.Date.values


# date_tickers=str(date_tickers).split('T').replace()
def format_date(x, pos):
    if x < 0 or x > len(date_tickers) - 1:
        return ''
    return str(date_tickers[int(x)]).replace('T00:00:00.000000000', '')


'''

plt.subplot2grid((6,4),(0,0),rowspan=4,colspan=4
(6,4:將圖分成6行4列,
(0,0):從0行0列開始畫圖
rowspan=4:占四個row
colspan=4：
#
'''

ax1 = plt.subplot2grid((6, 4), (0, 0), rowspan=4, colspan=4, facecolor='white')
# candlestick_ohlc(ax1,data_plot.values[-length:],width=0.6,colorup='red',colordown='green')
candlestick_ohlc(ax1, data_plot.values[-length:], width=0.6, colorup='red', colordown='green')
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# ax1.set_xticklabels(date_tickers)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
ax1.plot(data_plot['Date'].values[-length:], ma5[-length:], 'black', Label='5 MA', linewidth=1.5)
ax1.plot(data_plot['Date'].values[-length:], ma10[-length:], 'navy', Label='10 MA', linewidth=1.5)
ax1.plot(data_plot['Date'].values[-length:], ma20[-length:], 'yellow', Label='20 MA', linewidth=1.5)
ax1.legend(loc='upper center', ncol=3)
ax1.grid(True, color='black')
plt.ylabel('Stock Price & Volume')
plt.suptitle('Stock Code="2330"', color='black', fontsize=16)

# 畫KD值
ax2 = plt.subplot2grid((6, 4), (4, 0), sharex=ax1, rowspan=1, colspan=4, facecolor='white')
ax2.plot(data_plot['Date'].values[-length:], data_plot['K'].values[-length:], color='black')
ax2.plot(data_plot['Date'].values[-length:], data_plot['D'].values[-length:], color='navy')
plt.ylabel('KD Value')
'''
#成交量
ax2=plt.subplot2grid((6,4),(4,0),sharex=ax1,rowspan=1,colspan=4,facecolor='white')
ax2.bar(data_plot['Date'].values[-length:],data_plot['volume'].values[-length:],color='black',alpha=0.4)
plt.ylabel('volume')

'''
