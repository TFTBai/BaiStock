import pandas as pd
from common import constant as con

'''
 策略类
 用于筛选出股票后的操作模拟
 核心内容是按照固定的买卖策略买卖
 '''


class strategy:
    #买入价格
    buy_price = 0
    #卖出价格
    sell_price = 0
    #策略收益
    strategy_income = 0
    #是否卖出成功
    sell_sucess = False

def get_strategy_income(baseStockInfo,date):
    '''
        获得策略买卖收益
        策略收益=（买入价格-卖出价格）买入价格
        1.需要买入的价格
            ①从日期date开始按 买入策略买入，如果成功则赋值买入规则
            ②如果没买入成功则直接跳出循环 不计入
        2.需要卖出的价格
            ①按卖出策略卖出，可能存在以下特殊情况
                1)不足20天则直接跳出循环 不计入
                2)如果20天没有卖出 →割肉
    '''
    day_count = 0
    right_strategy = strategy()

    #可买出detail
    sell_days_detail = baseStockInfo[baseStockInfo['date'] > date]

    #计划买入价格
    buy_price = (baseStockInfo[baseStockInfo['date'] == date])['open'].tolist()[0]

    # 计划卖出价格
    sell_price = buy_price * 2000


    sell_date_list = sell_days_detail['date']
    #循环每一个可以卖的日期
    for sell_date in sell_date_list:
        sell_detail = sell_days_detail[sell_days_detail['date']==sell_date]
        day_count = day_count + 1
        #卖出策略
        #如果当日最高价高于策略卖出价 标记卖出成功!
        if(sell_detail['high'].tolist()[0] > sell_price):
            right_strategy.sell_sucess = True

        #如果当日开盘价高于 策略卖出价,则卖出价为开盘价,标记卖出成功!
        if(sell_detail['open'].tolist()[0]>sell_price):
            sell_price = sell_detail['open'].tolist()[0]
            right_strategy.sell_sucess = True

        #①如果交易日是day20 前面没卖出,则割肉收盘价卖
        if(day_count==2):
            if(right_strategy.sell_sucess == False):
                right_strategy.sell_sucess = True
                sell_price = sell_detail['close'].tolist()[0]

        # right_strategy.sell_sucess = True
        # sell_price = sell_detail['close'].tolist()[0]
        #如果卖出成功了,终止循环返回策略收益
        if(right_strategy.sell_sucess == True):
            right_strategy.buy_price = buy_price
            right_strategy.sell_price = sell_price
            right_strategy.strategy_income = (round(sell_price/buy_price,4)*100)-100
            return right_strategy
    return right_strategy
