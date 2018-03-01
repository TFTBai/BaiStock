'''
负责筛选规则后的展示
'''
from common import constant as con
import pandas as pd
from common import dateUtil,commonUtil
from rule import rule
import gc
import copy


# 增加正收益率百分比
def add_days_income_percent(df, rightStock):
    for day in con.day_list:
        # ptemp = rightStock['day' + str(day) + 'openIncome']
        # pCount = 0
        # percentDay = 0
        # for p in ptemp:
        #     if (p >= 0):
        #         pCount = pCount + 1
        # if (pCount != 0):
        #     percentDay = round(pCount / len(ptemp), 2) * 100
        # df['day' + str(day) + 'oip'] = percentDay

        ptemp = rightStock['day' + str(day) + 'closeIncome']
        pCount = 0
        percentDay = 0
        for p in ptemp:
            if (p >= 0):
                pCount = pCount + 1
        if (pCount != 0):
            percentDay = round(pCount / len(ptemp), 2) * 100
        df['day' + str(day) + 'cip'] = percentDay

        # ptemp = rightStock['day' + str(day) + 'highIncome']
        # pCount = 0
        # percentDay = 0
        # for p in ptemp:
        #     if (p >= 0):
        #         pCount = pCount + 1
        # if (pCount != 0):
        #     percentDay = round(pCount / len(ptemp), 2) * 100
        # df['day' + str(day) + 'hip'] = percentDay

    return df


# 增加最大价格出现日百分比
def add_max_price_day_percent(df, rightStock):
    max_price_day = rightStock['highestDay']
    length = len(max_price_day)
    for day in con.day_list:
        df['d' + str(day)] = round(len(rightStock[rightStock['highestDay'].isin([day])]) / length, 2) * 100
    return df


# 增加收入平均值
def add_income_mean(df, rightStock):
    for day in con.day_list:
        df['d' + str(day) + 'cMean'] = round(rightStock['day' + str(day) + 'closeIncome'].mean(), 2)
    for day in con.day_list:
        df['d' + str(day) + 'oMean'] = round(rightStock['day' + str(day) + 'openIncome'].mean(), 2)
    for day in con.day_list:
        df['d' + str(day) + 'hMean'] = round(rightStock['day' + str(day) + 'highIncome'].mean(), 2)
    return df


# 增加最高多少卖 卖不出再收盘卖 收益
def add_high_income_mean(df, rightStockH):
    for p in con.high_percent_list:
        mean = (df['d2hMean'] * p)[0]
        locals()['rightStock' + str(p)] = rightStockH[rightStockH['day2highIncome'] >= mean]
        locals()['rightStockE' + str(p)] = rightStockH[rightStockH['day2highIncome'] < mean]
        locals()['rightStock' + str(p)]['day2highIncome'] = mean
        locals()['rightStockE' + str(p)]['day2highIncome'] = locals()['rightStockE' + str(p)]['day2closeIncome']
        newRightStockH = locals()['rightStock' + str(p)].append(locals()['rightStockE' + str(p)])
        newRightStockH = group_by_date(newRightStockH)
        df[str(p) + 'day2MeanH'] = round(newRightStockH['day2highIncome'].mean(), 2)
    return df


# 如果第二日收盘卖不出,则按原价卖出
def add_final_income(df, rightStock,stockArgX,dfname):
    rightStockGood = rightStock[rightStock.day2closeIncome >= 0]
    rightStockNormal = rightStock[(rightStock.day2closeIncome < 0) &
                                  ((rightStock.day3highIncome >= 0)
                                   | (rightStock.day4highIncome >= 0)
                                   | (rightStock.day5highIncome >= 0)
                                   | (rightStock.day6highIncome >= 0)
                                   | (rightStock.day7highIncome >= 0)
                                   | (rightStock.day8highIncome >= 0)
                                   | (rightStock.day9highIncome >= 0)
                                   | (rightStock.day11highIncome >= 0)
                                   | (rightStock.day12highIncome >= 0)
                                   | (rightStock.day13highIncome >= 0)
                                   | (rightStock.day14highIncome >= 0)
                                   | (rightStock.day15highIncome >= 0)
                                   | (rightStock.day16highIncome >= 0)
                                   | (rightStock.day17highIncome >= 0)
                                   | (rightStock.day18highIncome >= 0)
                                   | (rightStock.day19highIncome >= 0)
                                   | (rightStock.day20highIncome >= 0)
                                   )]
    rightStockLoss = rightStock[(rightStock['day2highIncome'] < 0)
                                & (rightStock['day3highIncome'] < 0)
                                & (rightStock['day4highIncome'] < 0)
                                & (rightStock['day5highIncome'] < 0)
                                & (rightStock['day6highIncome'] < 0)
                                & (rightStock['day7highIncome'] < 0)
                                & (rightStock['day8highIncome'] < 0)
                                & (rightStock['day9highIncome'] < 0)
                                & (rightStock['day11highIncome'] < 0)
                                & (rightStock['day12highIncome'] < 0)
                                & (rightStock['day13highIncome'] < 0)
                                & (rightStock['day14highIncome'] < 0)
                                & (rightStock['day15highIncome'] < 0)
                                & (rightStock['day16highIncome'] < 0)
                                & (rightStock['day17highIncome'] < 0)
                                & (rightStock['day18highIncome'] < 0)
                                & (rightStock['day19highIncome'] < 0)
                                & (rightStock['day20highIncome'] < 0)
                                ]
    # 是否生产保本表
    if (stockArgX.save):
        rightStockGood.to_csv(con.detailPath + str(
            dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + dfname + 'day2收盘卖.csv', index=False)
        rightStockNormal.to_csv(
            con.detailPath + str(dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + dfname + '原价卖.csv',
            index=False)
        rightStockLoss.to_csv(
            con.detailPath + str(dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + dfname + '割肉卖.csv',
            index=False)

    #进行日期分组
    rightStockGood = group_by_date(rightStockGood)
    rightStockNormal = group_by_date(rightStockNormal)
    rightStockLoss = group_by_date(rightStockLoss)


    #分组后计算收益和概率
    totalCount = len(rightStockGood)  + len(rightStockNormal) + len(rightStockLoss)
    df['day2收盘卖掉概率'] = round(len(rightStockGood) / totalCount, 3)
    df['原价卖概率'] = round(len(rightStockNormal) / totalCount, 3)
    df['割肉卖概率'] = round(len(rightStockLoss) / totalCount, 3)

    df['day2收盘卖掉平均收益'] = round(rightStockGood.day2closeIncome.mean(),3)
    df['原价卖收益'] = 0
    df['割肉卖平均亏损'] = round(rightStockLoss.day20closeIncome.mean(),3)

    df['保本卖法收益'] = round((df['day2收盘卖掉概率'] * (df['day2收盘卖掉平均收益'] + 1)) + df['原价卖概率'] + (df['割肉卖概率'] * (df['割肉卖平均亏损'] + 1)),3)

    return df


# 增加筛选规则对应的样本数量显示
def add_right_count(df, rightstock):
    all_count = len(rightstock)
    df['totalCount'] = all_count
    df['totalCountP'] = round(all_count / 420000, 4) * 100
    return df


# 增加筛选规则对应的样本数量显示
def add_right_count_by_date(df, rightstock):
    all_count = len(rightstock)
    df['dateCount'] = all_count
    df['dateCountP'] = round(all_count / 1824, 4) * 100
    return df


# 增加按日期分组
def group_by_date(rightstock):
    rightstock = rightstock.groupby('date').mean()
    return rightstock


'''
生成某规则的total报表数据

'''
def get_total_csv(rightStock, dfname, stockArgX):
    rightStocklist = [dfname]
    totalProfit = pd.DataFrame({'rule': rightStocklist})

    if(stockArgX.strategy == True):
        #复制一份原始stock，用于策略买卖收益
        rightStockStrategy = copy.deepcopy(rightStock)
        totalProfit = rule.add_strategy_income(totalProfit,rightStockStrategy,stockArgX,dfname)

    #复制一份原始stock,用于计算原价卖收益
    # rightStockH = copy.deepcopy(rightStock)
    #计算原价卖收益
    # totalProfit = add_final_income(totalProfit, rightStockH,stockArgX,dfname)
    totalProfit = add_right_count(totalProfit, rightStock)
    rightStock = group_by_date(rightStock)
    # 是否生产中间表
    if (stockArgX.mean):
        rightStock.to_csv(
            con.detailPath + str(dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + dfname + 'mean.csv',
            index=False)
    # 增加筛选规则对应的样本数量和百分百显示
    totalProfit = add_right_count_by_date(totalProfit, rightStock)
    # 计算并且增加 评价收益
    totalProfit = add_income_mean(totalProfit, rightStock)
    totalProfit = add_days_income_percent(totalProfit, rightStock)
    # totalProfit = add_high_income_mean(totalProfit,rightStockH)
    # totalProfit = add_max_price_day_percent(totalProfit, rightStock)

    # 清除临时detail缓存
    del rightStock
    # 马上重置垃圾清除器
    gc.collect()
    return totalProfit


'''
生成某规则的total报表数据

'''


def get_total_csv_by_year(rightStock, ruleName, stockArgX, totalReportForm):
    rightStockList = []

    '''
    先进行按年划分
    '''

    rightStock1 = rightStock[rightStock['date'] >= '2010-01-01']
    rightStock1 = rightStock1[rightStock1['date'] < '2011-01-01']

    rightStock2 = rightStock[rightStock['date'] >= '2011-01-01']
    rightStock2 = rightStock2[rightStock2['date'] < '2012-01-01']

    rightStock3 = rightStock[rightStock['date'] >= '2012-01-01']
    rightStock3 = rightStock3[rightStock3['date'] < '2013-01-01']

    rightStock4 = rightStock[rightStock['date'] >= '2013-01-01']
    rightStock4 = rightStock4[rightStock4['date'] < '2014-01-01']

    rightStock5 = rightStock[rightStock['date'] >= '2014-01-01']
    rightStock5 = rightStock5[rightStock5['date'] < '2015-01-01']

    rightStock6 = rightStock[rightStock['date'] >= '2015-01-01']
    rightStock6 = rightStock6[rightStock6['date'] < '2016-01-01']

    rightStock7 = rightStock[rightStock['date'] >= '2016-01-01']
    rightStock7 = rightStock7[rightStock7['date'] < '2017-01-01']

    rightStock8 = rightStock[rightStock['date'] >= '2017-01-01']
    rightStock8 = rightStock8[rightStock8['date'] < '2018-01-01']

    rightStockList.append(rightStock)
    rightStockList.append(rightStock1)
    rightStockList.append(rightStock2)
    rightStockList.append(rightStock3)
    rightStockList.append(rightStock4)
    rightStockList.append(rightStock5)
    rightStockList.append(rightStock6)
    rightStockList.append(rightStock7)
    rightStockList.append(rightStock8)

    year = -2
    '''
    再循环添加对应的数据
    '''
    for rightStockX in rightStockList:
        year = year + 1
        if len(rightStockX) > 0:
            ruleNameyear = ruleName + 'year201' + str(year)
            # 如果是全部的rightStock 则重新命名为 year
            if (year == -1):
                ruleNameyear = ruleName + 'year'
            ruleNamelist = [ruleNameyear]
            totalProfit = pd.DataFrame({'rule': ruleNamelist})

            totalProfit = add_right_count(totalProfit, rightStockX)
            rightStockX = group_by_date(rightStockX)
            # 是否生产中间表
            if (stockArgX.mean):
                rightStockX.to_csv(con.detailPath + str(
                    dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + ruleNameyear + 'mean.csv',
                                   index=False)
            # 增加筛选规则对应的样本数量和百分百显示
            totalProfit = add_right_count_by_date(totalProfit, rightStockX)
            # 计算并且增加 评价收益
            totalProfit = add_income_mean(totalProfit, rightStockX)
            totalProfit = add_days_income_percent(totalProfit, rightStockX)
            totalReportForm = totalReportForm.append(totalProfit)
            # 清除临时detail缓存
            del rightStockX
            # 马上重置垃圾清除器
            gc.collect()
    del rightStock
    # 马上重置垃圾清除器
    gc.collect()
    return totalReportForm


'''
生成detail报表
'''


def generate_detail_csv(detailTempList, stockArgX, ruleName):
    # 8.如果规则筛选出了样本则进行生成csv等
    if (len(detailTempList) > 0):
        # 连接所有的detail数据
        tempDetail = pd.concat(detailTempList)
        # 转换为pandas的dataframe格式
        tempDetail = pd.DataFrame(tempDetail)
        # 按日期逆向排序
        tempDetail = tempDetail.sort_values(by=['date'], ascending=False)
        # 10.是否生成detail表
        if (stockArgX.detail and len(tempDetail) > 0):
            tempDetail.to_csv(con.detailPath + str(dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + ruleName + 'detail.csv',
                              index=False)
        #为邮件保存临时detail
        stockArgX.tempDetail = tempDetail
        return tempDetail
