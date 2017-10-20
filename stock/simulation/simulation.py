from common import commonUtil

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
    sell_success = False
    #第几天卖出的
    sell_day = 0

def get_strategy_income(baseStockInfo,date,stockArgX):
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

    #day0 detail
    signal_days_detail = baseStockInfo[baseStockInfo['date'] == date]
    #可卖出detail
    sell_days_detail = baseStockInfo[baseStockInfo['date'] > date]

    if(len(sell_days_detail)<1):
        return right_strategy

    buy_price = 0
    sell_price = 0
    lowest = 1000

    if(stockArgX.buyLineTF==True):
        # day0 close价格
        signal_close_price = signal_days_detail['close'].tolist()[0]
        # 买入线价格
        buy_line_price = signal_close_price * commonUtil.get_multiple_by_percentage(stockArgX.buyLine)
        # 买入线期望价格
        buy_line_price_expect = signal_close_price * commonUtil.get_multiple_by_percentage(stockArgX.buyLine+stockArgX.buyLineExpect)
    else:
        # 计划买入价格
        buy_price = sell_days_detail.head(1)['open'].tolist()[0]

    sell_date_list = sell_days_detail['date']
    #循环每一个可以卖的日期
    for sell_date in sell_date_list:
        sell_detail = sell_days_detail[sell_days_detail['date']==sell_date]
        day_count = day_count + 1
        #是否使用买入线策略
        if (stockArgX.buyLineTF == True):
            #只有买入价格为0的时候,才进行赋值判断
            if(buy_price == 0):
                #如果day几大于等待天数,直接买入失败
                if(day_count > stockArgX.buyLineWaitDays):
                    right_strategy.sell_success = False
                    return right_strategy
                if(sell_detail['low'].tolist()[0] < buy_line_price):
                    buy_price = buy_line_price_expect
                else:
                    continue

        #day1不可以卖
        if(day_count==1):
            continue

        # 只有当卖出价格为0时候计算,避免覆盖
        if (sell_price == 0):
            # 固定收益卖出价
            if (stockArgX.sellIncomeTF == True):
                sell_price = buy_price * commonUtil.get_multiple_by_percentage(stockArgX.sellIncome)
            # 按low收益卖出价
            if (stockArgX.sellIncomeByLowTF == True):
                low = sell_detail['low'].tolist()[0]
                if(low<lowest):
                    lowest = low
                sell_price = lowest + (buy_price * commonUtil.get_multiple_by_percentage(stockArgX.sellIncomeByLow)) - buy_price
            if (stockArgX.stopLineTF == True):
                # 止损线价格
                stop_line_price = buy_price * commonUtil.get_multiple_by_percentage(stockArgX.stopLine)
                # 止损线期望价格
                stop_line_expect_price = buy_price * commonUtil.get_multiple_by_percentage(
                    stockArgX.stopLine + stockArgX.stopLineExpect)

        #卖出策略
        #如果当日最高价高于策略卖出价 标记卖出成功!
        if(sell_detail['high'].tolist()[0] > sell_price):
            right_strategy.sell_success = True

        #如果当日开盘价高于 策略卖出价,则卖出价为开盘价,标记卖出成功!
        if(sell_detail['open'].tolist()[0]>sell_price):
            sell_price = sell_detail['open'].tolist()[0]
            right_strategy.sell_success = True

        #是否使用止损线策略
        if(stockArgX.stopLineTF == True):
            #如果当日最低价低于止损线,则卖出价位止损线期望价格
            if(sell_detail['low'].tolist()[0]<stop_line_price):
                sell_price = stop_line_expect_price
                right_strategy.sell_success = True

        #①如果交易日是day-cutMeatDay 前面没卖出,则割肉收盘价卖
        if(day_count==(stockArgX.cutMeatDay)):
            if(right_strategy.sell_success == False):
                right_strategy.sell_success = True
                sell_price = sell_detail['close'].tolist()[0]

        #如果卖出成功了,终止循环返回策略收益
        if(right_strategy.sell_success == True):
            right_strategy.buy_price = buy_price
            right_strategy.sell_price = sell_price
            right_strategy.strategy_income = (round(sell_price/buy_price,5)*100)-100
            right_strategy.sell_day = day_count
            return right_strategy
    return right_strategy
