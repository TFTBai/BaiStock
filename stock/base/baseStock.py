import tushare as ts
import pandas as pd
from common import mylog as log
from calculate import calculate as cal
from common import constant as con


# 生成本地base表数据

def create_base():
    stock_data = ts.get_today_all()
    stock_data.to_csv(con.basePath + 'base.csv', encoding='gbk')


# 查询单stock历史所有数据
def create_stock_csv(codeStr):
    log.info("当前开始生成代码" + codeStr + "的CSV文件!")
    stock_data = ts.get_k_data(codeStr, start='2010-01-01', end='2016-12-31')
    stock_data.to_csv(con.csvPath + codeStr + '.csv', index=False, encoding='utf-8')


# 获取所有的code
def get_all_code():
    df = pd.read_csv(con.basePath + 'base.csv', encoding='gbk')
    return df


# 生成所有stock基础数据csv
def create_all_stock_csv():
    # 获取所有的code
    allCode = get_all_code()
    # 循环当前所有stock 生成所有stock本地csv
    for code in allCode.code:
        # if (code == 1):
            codeStr = str(code).zfill(6)
            # 查询单stock历史所有数据
            create_stock_csv(codeStr)
    log.info("所有stock基础数据生成完毕!")


'''
增加衍生数据
'''
def add_derivative_data(stock_data):
    # 天假d1开/d0收值
    stock_data = cal.get_d1od0c(stock_data)
    # 添加5、10、20、30、60日线
    stock_data = cal.get_30days(stock_data)
    # # 4.计算每一个stock的kdj数据
    stock_data = cal.get_kdj(stock_data)
    # 5.计算么一个stock的macd值
    stock_data = cal.get_macd(stock_data)
    # 6.计算每一个stock的rsi值
    stock_data = cal.get_rsi(stock_data)
    # 添加收益
    stock_data = cal.get_firstDay_income(stock_data)
    return stock_data

'''
1.添加30日线数据
2.添加开盘卖收益
3.添加收盘卖收益
4.添加最高价卖收益
5.以及2-7日，最高价位是哪天
6.为所有的stock数据增加kdj macd rsi数据
'''


def add_stock_derivative_data():
    count = 0
    # 1.读取base文件获取所有的csv文件名=code
    allCode = get_all_code()
    # 2.循环所有的csv文件
    for code in allCode.code:
        # if (code == 1):
            count = count + 1
            codeStr = str(code).zfill(6)
            # 3.读取本地csv数据
            stock_data = pd.read_csv(con.csvPath + codeStr + '.csv')
            # 近期数据补全
            stock_data = cal.get_lost_data(stock_data, codeStr, False)
            # 增加衍生数据
            stock_data = add_derivative_data(stock_data)
            # 7.将计算好的kdj写入对应csv中
            stock_data.to_csv(con.csvPath + codeStr + '.csv', index=False)
            log.info('已生成代码' + codeStr + '的衍生数据,生成总数量' + str(count))
    log.info("为所有的stock增加衍生数据完毕!")


'''
增加指数衍生数据
'''
def add_index_derivative_data():
    count = 0
    # 2.循环所有的csv文件
    for codeStr in con.baseIndexList:
        count = count + 1
        # 3.读取本地csv数据
        stock_data = pd.read_csv(con.indexCsvPath + codeStr + '.csv')
        # 近期数据补全
        stock_data = cal.get_lost_data(stock_data, codeStr, False)
        # 增加衍生数据
        stock_data = add_derivative_data(stock_data)
        # 7.将计算好的kdj写入对应csv中
        stock_data.to_csv(con.indexCsvPath + codeStr + '.csv', index=False)
        log.info('已生成代码' + codeStr + '的衍生数据,生成总数量' + str(count))
    log.info("为所有的index增加衍生数据完毕!")


'''
修改基础数据 保留字段
'''


def update_all_stock():
    count = 0
    # 1.读取base文件获取所有的csv文件名=code
    allCode = get_all_code()
    # 2.循环所有的csv文件
    for code in allCode.code:
        # if (code == 1):
            count = count + 1
            codeStr = str(code).zfill(6)
            # 3.读取本地csv数据
            stock_data = pd.read_csv(con.csvPath + codeStr + '.csv')
            # 输出到csv
            stock_data.to_csv(con.csvPath + codeStr + '.csv', index=False,
                              columns=['date', 'code', 'open', 'close', 'high', 'low', 'volume', 'day1o/day0c',
                                       'day1highIncome', 'day1closeIncome',
                                       'day2highIncome', 'day2closeIncome', 'day3highIncome',
                                       'day3closeIncome', 'day4highIncome', 'day4closeIncome',
                                       'day5highIncome', 'day5closeIncome', 'day6highIncome', 'day6closeIncome', '2days',
                                       '5days',
                                       '30days', '60days',
                                       'kdj_k', 'kdj_d', 'kdj_j', 'macd', 'macd_DIFF', 'macd_DEA', 'rsi6', 'rsi12',
                                       'rsi24'])
            log.info('已重新生成' + codeStr + '的stock数据,生成总数量' + str(count))
    log.info("所有stock数据更新完毕!")


'''
获取并生成所有的base数据code放入内存中
'''


def put_base_csv_code_into_cash():
    # 0.声明base csv缓存用来存储code数据
    baseCodeList = []
    # 1.读取base文件获取所有的csv文件名=code
    allCode = get_all_code()
    # 2.循环所有的code
    count = 0
    for code in allCode.code:
        count = count+1
        if count > 100:
          return baseCodeList
        codeStr = str(code).zfill(6)
        baseCodeList.append(codeStr)
    return baseCodeList


'''
获取今日数据
'''


def get_today_stock():
    # 获取今日数据
    today_stock_data = ts.get_today_all()
    return today_stock_data


'''创建3大盘指数csv'''


def create_all_index_csv():
    for codeStr in con.baseIndexList:
        log.info("当前开始生成指数" + codeStr + "的CSV文件!")
        index_data = ts.get_k_data(codeStr, index=True, start='2010-01-01', end='2016-12-31')
        index_data.to_csv(con.indexCsvPath + codeStr + '.csv', index=False, encoding='utf-8')

