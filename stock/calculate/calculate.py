import pandas as pd
import talib as ta
import numpy as np
import tushare as ts
from common import constant as con


# 计算kdj值并add到stock_data中
def get_kdj(stock_data):
    # kdj计算
    low_list = pd.rolling_min(stock_data['low'], 9)
    low_list.fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
    high_list = pd.rolling_max(stock_data['high'], 9)
    high_list.fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
    rsv = (stock_data['close'] - low_list) / (high_list - low_list) * 100
    # 增加kdj数据到 stock_data中
    stock_data['kdj_k'] = round(pd.ewma(rsv, com=2), 2)
    stock_data['kdj_d'] = round(pd.ewma(stock_data['kdj_k'], com=2), 2)
    stock_data['kdj_j'] = round(3 * stock_data['kdj_k'] - 2 * stock_data['kdj_d'], 2)
    return stock_data


# 计算macd值并add到stock_data中
def get_macd(stock_data):
    # 参数12,26,9
    macd, macdsignal, macdhist = ta.MACD(np.array(stock_data['close']), fastperiod=12, slowperiod=26, signalperiod=9)
    # 13-15 DIFF  DEA  DIFF-DEA
    stock_data['macd'] = round(pd.Series(macdhist, index=stock_data.index) * 2, 2)  # DIFF-DEA
    stock_data['macd_DIFF'] = round(pd.Series(macd, index=stock_data.index), 2)  # DIFF
    stock_data['macd_DEA'] = round(pd.Series(macdsignal, index=stock_data.index), 2)  # DEA
    return stock_data


# 计算rsi值并add到stock_data中
def get_rsi(stock_data):
    rsi6 = ta.RSI(np.array(stock_data['close']), timeperiod=6)
    rsi12 = ta.RSI(np.array(stock_data['close']), timeperiod=12)
    rsi24 = ta.RSI(np.array(stock_data['close']), timeperiod=24)
    stock_data['rsi6'] = round(pd.Series(rsi6, index=stock_data.index), 2)
    stock_data['rsi12'] = round(pd.Series(rsi12, index=stock_data.index), 2)
    stock_data['rsi24'] = round(pd.Series(rsi24, index=stock_data.index), 2)
    return stock_data


# 获取5、30、60日线数据
def get_date_line(stock_data):
    stock_data['2days'] = round(pd.rolling_mean(stock_data['close'], 2), 2)
    stock_data['5days'] = round(pd.rolling_mean(stock_data['close'], 5), 2)
    stock_data['30days'] = round(pd.rolling_mean(stock_data['close'], 30), 2)
    stock_data['60days'] = round(pd.rolling_mean(stock_data['close'], 60), 2)
    return stock_data

'''
获取5、10、30交易量日线
'''
def add_volume_date_line(stock_data):
    stock_data['volume5days'] = round(pd.rolling_mean(stock_data['volume'], 5), 2)
    stock_data['volume10days'] = round(pd.rolling_mean(stock_data['volume'], 10), 2)
    stock_data['volume30days'] = round(pd.rolling_mean(stock_data['volume'], 30), 2)
    return stock_data

'''
获取价格变动
'''
def add_price_change(stock_data):
    stock_data['price_change'] = round(stock_data['close']-stock_data['close'].shift(), 2)
    return stock_data

'''
获取涨跌幅
'''
def add_p_change(stock_data):
    stock_data['p_change'] = round((stock_data['close']/stock_data['close'].shift())-1, 2)
    return stock_data



'''
1.获取6天 最高收益 收盘收益
2.以及2-7日，最高价位是哪天
'''


def get_income(stock_data):
    highestDay = stock_data['high'].shift(-1)
    stock_data['highestDay'] = 1
    # 每一个都跟前一天对比
    for day in con.day_list:
        # 暂时先去掉日期和日期的开收价格
        # stock_data['day' + str(day)] = stock_data['date'].shift(-day)
        # stock_data['day' + str(day) + 'open'] = stock_data['open'].shift(-day)
        # stock_data['day' + str(day) + 'high'] = stock_data['high'].shift(-day)
        # stock_data['day' + str(day) + 'close'] = stock_data['close'].shift(-day)
        stock_data['day' + str(day) + 'openIncome'] = round(
            stock_data['open'].shift(-day) / stock_data['open'].shift(-day + 1),
            4) * 100 - 100
        stock_data['day' + str(day) + 'highIncome'] = round(
            stock_data['high'].shift(-day) / stock_data['open'].shift(-day + 1),
            4) * 100 - 100
        stock_data['day' + str(day) + 'closeIncome'] = round(
            stock_data['close'].shift(-day) / stock_data['open'].shift(-day + 1),
            4) * 100 - 100
        if (day != 1):
            temp = (stock_data['day' + str(day) + 'high'] > highestDay)
            stock_data['highestDay'] = stock_data['highestDay'] + temp
        del stock_data['day' + str(day) + 'high']
    return stock_data


# 补偿公式
def compensate_formula(x):
    return round((1 - (100 / (100 + x))) * 100, 3)


# 补偿负收益未连续计算
def compensate(stock_data, stock_data_income):
    stock_dataf = stock_data[stock_data[stock_data_income] < 0]
    stock_dataz = stock_data[stock_data[stock_data_income] >= 0]
    stock_dataNan = stock_data[stock_data[stock_data_income].isnull()]
    stock_dataf[stock_data_income] = compensate_formula(stock_dataf[stock_data_income])
    stock_data = stock_dataf.append(stock_dataz).append(stock_dataNan)
    return stock_data


# 跟第一天开盘做比较计算收益
def get_firstDay_income(stock_data):
    for day in con.day_list:
        stock_data['day' + str(day) + 'openIncome'] = round(
            stock_data['open'].shift(-day) / stock_data['open'].shift(-1),
            4) * 100 - 100
        stock_data['day' + str(day) + 'highIncome'] = round(
            stock_data['high'].shift(-day) / stock_data['open'].shift(-1),
            4) * 100 - 100
        stock_data['day' + str(day) + 'closeIncome'] = round(
            stock_data['close'].shift(-day) / stock_data['open'].shift(-1),
            4) * 100 - 100
    for day in con.day_list:
        stock_data = compensate(stock_data, 'day' + str(day) + 'openIncome')
        stock_data = compensate(stock_data, 'day' + str(day) + 'highIncome')
        stock_data = compensate(stock_data, 'day' + str(day) + 'closeIncome')
    stock_data = stock_data.sort(columns='date')
    return stock_data


# 计算day1开盘比day0收
def get_d1od0c(stock_data):
    stock_data['day1o/day0c'] = round(stock_data['open'].shift(-1) / stock_data['close'], 4) * 100 - 100
    return stock_data


# 补全近期数据
def get_lost_data(stock_data, codeStr, index):
    stock_data = stock_data[stock_data['date'] <= '2016-12-31']
    stock_data_lost = ts.get_k_data(codeStr, index=index)
    stock_data_lost = stock_data_lost[stock_data_lost['date'] > '2016-12-31']
    return stock_data.append(stock_data_lost)

