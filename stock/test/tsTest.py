import tushare as ts
import pandas as pd
from common import constant as con


# 按时间查询
def get_k_data(code):
    df = ts.get_k_data(code, start='2016-12-01', end='2017-02-05')
    print(df)
    return df


# 历史数据全查询
def get_hist_data(code):
    df = ts.get_hist_data(code)
    print(df)
    return df


# 基础数据
def get_stock_basics():
    df = ts.get_stock_basics()
    df.to_csv("d:/stock/basic.csv")
    return df


# 获取今日数据
def get_today_all():
    df = ts.get_today_all()
    df.to_csv("D:/workSpace/python/stock/base/today.csv", encoding='utf-8', index=False)
    return df


# 获取某个csv数据
def get_csv():
    df = pd.read_csv("D:/workSpace/python/stock/base/today.csv")
    print(df)


# 测试两个csv按日期合并
def get_csv():
    df = pd.read_csv(con.csvPath + '900951.csv')
    print(df)
    df2 = pd.read_csv(con.csvPath + '900930.csv')
    print(df2)
    df3 = pd.merge(df, df2,how='left',on=['date'])
    print(df3)
    df3.to_csv(con.csvPath + 'ffff' + '.csv', index=False, encoding='utf-8')


