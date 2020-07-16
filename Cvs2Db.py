#！/usr/bin/env python
# -*- conding:utf-8 -*-
###########################################
#Time : 2020/7/7 13:10
#Author: Simon Chen
#File : Cvs2Db.py
###########################################
import pandas as pd
import sqlite3
import glob
import datetime
import time
import platform
import os

#
# glob 套件是用來查找符合特定規則的文件名，以下是用來查找csv為副當名的文件，並存成list
#
year="2004"
#设定工作目录
if platform.system()== "Windows":
    print(platform.system())
    WorkDir = os.getcwd() + "\\..\\Data-twse\\"
#    CsvDir=WorkDir+'test_csv\\'+year+"\\"
    CsvDir=WorkDir+'csv\\'+year+"\\"
    DataBaseDir = WorkDir + 'DataBase\\'
else:
    print(platform.system())
    WorkDir = os.getcwd() + "/../Data-twse/"
    # CsvDir=WorkDir+'test_csv\\'
    CsvDir = WorkDir + 'csv/'+year+'/'
    DataBaseDir = WorkDir + 'DataBase/'

DateDataBaseName = DataBaseDir + 'TwStock-Date-'+year+'.db'
StockNoDbName = DataBaseDir + 'TwStock-No-'+year+'.db'
print("WorkDir="+WorkDir)
print("CSVDir="+CsvDir)
if os.path.isfile(DateDataBaseName):
    print("Date db %s exist" %(DateDataBaseName))
else:
    print('%s not exist' %(DateDataBaseName))

if os.path.isfile(StockNoDbName):
    print("Code db %s exist" %(StockNoDbName))
else:
    print('%s not exist' %(StockNoDbName))

all_csv_file=glob.glob(CsvDir+'*.csv')
#all_csv_file=all_csv_file.replace(remoced_path,"")
i=0
for filename in all_csv_file:
    print("filename="+filename)
#    filename=filename.replace(removed_path,'')
    all_csv_file[i]=all_csv_file[i].replace(CsvDir,"")
    i=i+1
#all_csv_file[0]=all_csv_file[0].replace(removed_path,"")


#連接資料庫，如果不存在會新建一個資料庫
db1=sqlite3.connect(DateDataBaseName)

#讀取所有csv資料並寫到資料庫

for file_name in all_csv_file:
    print(file_name)
    df=pd.read_csv(CsvDir+file_name).iloc[:,1:].to_sql(file_name.replace('.csv',''),db1,if_exists='replace')

#從資料庫讀回表單
#print(all_csv_file[0])
#pd.read_sql(con=db1,sql='SELECT * FROM "20040212"')
#print(pd.DataFrame)

#以個股代碼為Index的表單
date_list=[filename.replace(".csv",'') for filename in all_csv_file ]
print("data_list[0]="+date_list[0])
print("data_list[1]="+date_list[1])
print("data_list[2]="+date_list[2])
pd.read_sql(con=db1,sql='SELECT * FROM'+ '"'+date_list[2]+'"')
print(pd.DataFrame)

# 先從前面的資料讀取表格，整合成一張大表格,增加日期欄位
total_df= pd.DataFrame()

for date in date_list:
    print(date)
    df=pd.read_sql(con=db1,sql='SELECT * FROM'+ '"'+date+'"')
    df['Date']=date
    total_df=total_df.append(df)
print(total_df)


StockNoDb=sqlite3.connect(StockNoDbName)
total_dict=dict(tuple(total_df.groupby('證券代號')))
for key in total_dict.keys():
    print(key)
    df=total_dict[key].iloc[:,2:]
    df['Date']=pd.to_datetime(df['Date'])
    df=df.sort_values(by=['Date'])
#    df.to_sql(key,StockNoDb,if_exists='append')
    df.to_sql(key,StockNoDb,if_exists='replace')
#print(df)
#df=pd.read_csv(CsvDir+file_name).iloc[:,1:].to_sql(file_name.replace('.csv',''),db1,if_exists='replace')

