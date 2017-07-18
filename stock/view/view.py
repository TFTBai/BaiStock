'''
负责筛选规则后的展示
'''
from common import constant as con
import pandas as pd
import copy


#
# rightStock.columns = ['序号', '日期', '开盘价', '收盘价', '最高价', '最低价', '量', '股票代码', 'kdj_k', 'kdj_d', 'kdj_j', 'macd',
#                       'macd_DIFF', 'macd_DEA', 'rsi6', 'rsi12', 'rsi24', '第1天开盘价', '第1天日期', '第1天收益', '第2天日期',
#                       '第2天收益', '第3天日期', '第3天收益', '第4天日期', '第4天收益', '第5天日期', '第5天收益', '第6天日期', '第6天收益', '第7天日期',
#                       '第7天收益', 'kdj小于20', 'j大于前一天',
#                       'd-j<3', 'k-j<3', 'macd<0', '|macd/2|<3', 'diff大于前一天', 'rsi6、rsi12、rsi24<50',
#                       '|rsi6-rsi12|<3',
#                       '|rsi6-RSI24|<5']

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

        ptemp = rightStock['day' + str(day) + 'highIncome']
        pCount = 0
        percentDay = 0
        for p in ptemp:
            if (p >= 0):
                pCount = pCount + 1
        if (pCount != 0):
            percentDay = round(pCount / len(ptemp), 2) * 100
        df['day' + str(day) + 'hip'] = percentDay

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
    # for day in con.day_list:
    #     df['d' + str(day) + 'oMean'] = round(rightStock['day' + str(day) + 'openIncome'].mean(), 2)
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


# 总收益百分比和盈利能力
def add_final_income(df, rightStock):
    rightStockGood = rightStock[rightStock.day2closeIncome > 0]
    rightStockGoodNormal = rightStock[rightStock.day2closeIncome == 0]
    rightStockNormal = rightStock[(rightStock.day2closeIncome < 0) &
                                  ((rightStock.day3closeIncome >= 0)
                                   | (rightStock.day4closeIncome >= 0)
                                   | (rightStock.day5closeIncome >= 0)
                                   | (rightStock.day6closeIncome >= 0)
                                   | (rightStock.day7closeIncome >= 0)
                                   )]
    rightStockLoss = rightStock[(rightStock['day2highIncome'] < 0)
                                & (rightStock['day3highIncome'] < 0)
                                & (rightStock['day4highIncome'] < 0)
                                & (rightStock['day5highIncome'] < 0)
                                & (rightStock['day6highIncome'] < 0)
                                & (rightStock['day7highIncome'] < 0)
                                ]
    totalCount = len(rightStockGood) + len(rightStockGoodNormal) + len(rightStockNormal) + len(rightStockLoss)
    df['goodP'] = round(len(rightStockGood) / totalCount, 3)
    df['normalP'] = round((len(rightStockNormal) + len(rightStockGoodNormal)) / totalCount, 3)
    df['lossP'] = round(len(rightStockLoss) / totalCount, 3)
    df['goodI'] = rightStockGood.day2closeIncome.mean()
    df['normalI'] = 0
    df['lossI'] = rightStockLoss.day7closeIncome.mean()
    df['income'] = (df['goodP'] * (df['goodI'] + 1)) + df['normalP'] + (df['lossP'] * (df['lossI'] + 1))
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
生成总报表

'''


def get_total_csv(rightStock, dfname):
    rightStocklist = [dfname]
    df = pd.DataFrame({'rule': rightStocklist})
    # rightStockH = copy.deepcopy(rightStock)
    # df = add_final_income(df, rightStock)
    df = add_right_count(df, rightStock)
    rightStock = group_by_date(rightStock)
    #是否生产中间表
    if (False):
        rightStock.to_csv(con.detailPath + dfname + 'mean.csv',
                          index=False)
    #增加筛选规则对应的样本数量和百分百显示
    df = add_right_count_by_date(df, rightStock)
    #计算并且增加 评价收益
    df = add_income_mean(df, rightStock)
    df = add_days_income_percent(df, rightStock)
    # df = add_high_income_mean(df,rightStockH)
    # df = add_max_price_day_percent(df, rightStock)
    return df


'''
生成每次发生报表
'''
def get_detail_csv():
    return
