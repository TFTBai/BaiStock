import tushare as ts
import pandas as pd


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
