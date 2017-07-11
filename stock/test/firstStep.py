import tushare as ts
import pandas as pd
from common import dateCommon as dc


# 全局常量

# 工具类

# 计算某股票的每个日期kdj
def get_kdj(code):
    stock_data = ts.get_k_data(code)
    # kdj
    low_list = pd.rolling_min(stock_data['low'], 9)
    low_list.fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
    high_list = pd.rolling_max(stock_data['high'], 9)
    high_list.fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
    rsv = (stock_data['close'] - low_list) / (high_list - low_list) * 100
    stock_data['kdj_k'] = pd.ewma(rsv, com=2)
    stock_data['kdj_d'] = pd.ewma(stock_data['kdj_k'], com=2)
    stock_data['kdj_j'] = 3 * stock_data['kdj_k'] - 2 * stock_data['kdj_d']
    # 用今天的j值和昨天比较
    kdj_j = stock_data['kdj_j']
    yesterdayJ = kdj_j[kdj_j.size - 2]
    todayJ = kdj_j[kdj_j.size - 1]
    kdj_k = stock_data['kdj_k']
    todayK = kdj_k[kdj_k.size - 1]
    # 如果今天的j值大于昨天的j值才继续后面的逻辑
    if (todayJ > yesterdayJ and todayK < float(20)):
        # 计算价格5日百分比
        stock_data = stock_data[stock_data.date > str(dc.get_the_day_before_today(1))]
        stock_data['kdj_ok'] = 1
    else:
        stock_data = stock_data[stock_data.date > str(dc.get_the_day_before_today(1))]
        stock_data['kdj_ok'] = 0
    return stock_data

# 计算某股票的每个日期kdj
def get_kdj_history(code):
    stock_data = ts.get_k_data(code)
    # kdj
    low_list = pd.rolling_min(stock_data['low'], 9)
    low_list.fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
    high_list = pd.rolling_max(stock_data['high'], 9)
    high_list.fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
    rsv = (stock_data['close'] - low_list) / (high_list - low_list) * 100
    stock_data['kdj_k'] = round(pd.ewma(rsv, com=2), 2)
    stock_data['kdj_d'] = round(pd.ewma(stock_data['kdj_k'], com=2), 2)
    stock_data['kdj_j'] = round(3 * stock_data['kdj_k'] - 2 * stock_data['kdj_d'], 2)
    # 用今天的j值和昨天比较
    kdj_j = stock_data['kdj_j']
    if (kdj_j.size < 6):
        stock_data = stock_data.tail(1)
        stock_data['kdj_k'] = 0
        stock_data['kdj_ok'] = 0
        return stock_data
    yesterdayJ = kdj_j[kdj_j.size - 6]
    todayJ = kdj_j[kdj_j.size - 5]
    kdj_k = stock_data['kdj_k']
    todayK = kdj_k[kdj_k.size - 5]
    # 如果今天的j值大于昨天的j值才继续后面的逻辑
    if (todayJ > yesterdayJ and todayK < float(20)):
        # 计算价格5日百分比
        stock_data_copy = stock_data[:]
        stock_data_copy = stock_data_copy.tail(5)
        stock_data_copy['indexNum'] = [1, 2, 3, 4, 5]
        stock_data_copy = stock_data_copy.sort(columns='high')
        stock_data_copy = stock_data_copy.tail(1)
        maxValue = stock_data_copy.high.values
        maxDate = stock_data_copy.date.values
        stock_data = stock_data.tail(5)
        stock_data = stock_data.head(1)
        stock_data['kdj_ok'] = 1
        highPercent = maxValue / stock_data.close.values[0]
        stock_data['highPercent'] = (round(highPercent, 3) * 100) - 100
        stock_data['highDate'] = maxDate
        stock_data['highDays'] = stock_data_copy.indexNum.values
    else:
        stock_data = stock_data.tail(1)
        stock_data['kdj_ok'] = 0
    return stock_data


# 一、获取所有code信息
def get_all_code():
    df = pd.read_csv("d:/stock/base/base.csv")
    return df


def gogogo():
    codeCount = 0
    rightCount = 0
    count = 0
    # 执行
    allCode = get_all_code()
    sumCount = 3000
    # 二、循环取code值
    dfall = get_kdj_history('000001')
    for code in allCode.code:
        code = str(code)
        code = code.zfill(6)
        codeCount = codeCount + 1
        print('共' + str(sumCount) + '，当前计算的是' + str(code) + "已处理" + str(codeCount) + '个')
        df = get_kdj_history(code)
        if (len(df.kdj_k.values)):
            if (df.kdj_ok.values == 1):
                dfall = dfall.append(df)
                rightCount = rightCount + 1
                print('符合条件的个数为' + str(rightCount))
                count = count + 1
                if (count > 1):
                    break
    dfall = dfall.sort(columns='kdj_k')
    dfall.to_csv('d:/stock/kdj2.csv')

gogogo()
