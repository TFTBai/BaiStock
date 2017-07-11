from base import baseStock as bs
import pandas as pd
from common import constant as con
import itertools
import copy
from view import view
import datetime
import gc


# 循环列表 删除base中符合的code的行
# 对符合的删除前33行
# 循环时跳过第一行,从第二行开始算有效

def cut_by_rule(df):
    # kdj
    df['kdj小于20'] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
    df['j大于前一天'] = df['kdj_j'] > df['kdj_j'].shift()
    df['d-j<3'] = df['kdj_d'] - df['kdj_j'] < 3
    df['k-j<3'] = df['kdj_k'] - df['kdj_j'] < 5
    # macd
    df['macd<0'] = df['macd'] < 0
    df['|macd/2|<3'] = (-3 < (df['macd'] / 2)) & ((df['macd'] / 2) < 3)
    df['diff大于前一天'] = df['macd_DIFF'] > df['macd_DIFF'].shift()
    # rsi
    df['rsi6、rsi12、rsi24<50'] = (df['rsi6'] < 50) & (df['rsi12'] < 50) & (df['rsi24'] < 50)
    df['|rsi6-rsi12|<3'] = (-3 < (df['rsi6'] - df['rsi12'])) & ((df['rsi6'] - df['rsi12']) < 3)
    df['|rsi6-RSI24|<5'] = (-5 < (df['rsi6'] - df['rsi24'])) & ((df['rsi6'] - df['rsi24']) < 5)
    # 日线    ①日线小于30日均线的80%
    df['day<80%'] = round(df['close'] / df['30days'], 2) < 0.8

    # 筛选符合条件的日期
    df = df[(df['kdj小于20'] == True) & (df['j大于前一天'] == True) & (df['d-j<3'] == True) & (df['k-j<3'] == True)
            & (df['macd<0'] == True) & (df['|macd/2|<3'] == True) & (df['diff大于前一天'] == True)
            & (df['rsi6、rsi12、rsi24<50'] == True) & (df['|rsi6-rsi12|<3'] == True) & (df['|rsi6-RSI24|<5'] == True)
            & (df['day<80%'] == True)]
    return df


'''
第二套规则
一、KDJ
    ①kdj小于20
    ②j第0日-前一日>5
    ③0<d-j<3
    ④0<k-j<5
    ⑤0<k-d<3
    ⑥j前日-大前日>3
    ⑦（k当日-前日）>（k前日-大前日）
二、日线
'''


def cut_by_30days(df):
    # 日线    ①日线小于30日均线的80%
    df['day<80%'] = round(df['close'] / df['30days'], 2) < 0.8
    df['kdj小于20'] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
    df['j当日-前一日>5'] = df['kdj_j'] - df['kdj_j'].shift() > 5
    df['0<d-j<3'] = (df['kdj_d'] - df['kdj_j'] < 3) & (df['kdj_d'] - df['kdj_j'] > 0)
    df['0<k-j<5'] = (df['kdj_k'] - df['kdj_j'] < 5) & (df['kdj_d'] - df['kdj_j'] > 0)
    df['0<k-d<3'] = (df['kdj_k'] - df['kdj_d'] < 3) & (df['kdj_d'] - df['kdj_j'] > 0)
    df['j前日-大前日>3'] = (df['kdj_j'].shift() - df['kdj_j'].shift().shift()) > 3
    df['（k当日-前日）>（k前日-大前日)'] = (df['kdj_k'] - df['kdj_k'].shift()) - (
        df['kdj_k'].shift() - df['kdj_k'].shift().shift()) > 0
    # 筛选符合条件的日期
    df = df[((df['day<80%'] == True)
             & (df['kdj小于20'] == True)
             & (df['j当日-前一日>5'] == True)
             & (df['0<d-j<3'] == True)
             & (df['0<k-j<5'] == True)
             & (df['0<k-d<3'] == True)
             & (df['j前日-大前日>3'] == True)
             & (df['（k当日-前日）>（k前日-大前日)'] == True))
    ]
    return df


# 8公里规则
def use_rule_8km(df):
    # 日线    ①日线小于30日均线的80%
    df['day<80%'] = round(df['close'] / df['30days'], 2) < 0.80
    df['kdj小于20'] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
    df['j大于前一天'] = df['kdj_j'] > df['kdj_j'].shift()
    df['macd大于前一天'] = df['macd'] > df['macd'].shift()
    df = df[(df['day<80%'] == True)
            & (df['kdj小于20'] == True)
            & (df['j大于前一天'] == True)
            & (df['macd大于前一天'] == True)
            ]
    return df


def find_right_stock():
    count = 0
    allCode = bs.get_all_code()
    rightStock = pd.DataFrame()
    for code in allCode.code:
        codeStr = str(code).zfill(6)
        print('开始筛选' + codeStr + '已经筛选了' + str(count))
        stock_data = pd.read_csv(con.csvPath + codeStr + '.csv')
        count = count + 1
        if stock_data.empty:
            continue
            # rightStock = rightStock.append(stock_data, ignore_index=True)
    return rightStock


## 获取成熟规则list
def get_total_list():
    allList = []
    df = pd.read_csv(con.detailPath + '2017-03-23total模拟开始纪念版数据收益.csv')
    ruleLists = df['rule']
    count = 0
    for ruleList in ruleLists:
        count = count + 1
        ruleList = ruleList.replace('rule', '')
        ruleList = ruleList.replace('+10', '')
        ruleList = ruleList.replace('+', ',')
        ruleList = ruleList.replace('-', ',')
        ruleList = ruleList.replace(',', '', 1)
        list(ruleList)
        tempList = ruleList.split(',')
        rightList = []
        for rule in tempList:
            ruleInt = int(rule)
            rightList.append(ruleInt)
        allList.append(rightList)
    return allList



def get_all_rule(allList):
    class rule:
        num = 0
        name = ''

    rule1 = rule()
    rule1.tf = True
    rule1.num = 1
    rule1.name = '日线小于30日线的75%'

    rule2 = rule()
    rule2.tf = True
    rule2.num = 2
    rule2.name = '日线小于30日线的80%'

    rule3 = rule()
    rule3.tf = True
    rule3.num = 3
    rule3.name = 'j大于前一天'

    rule4 = rule()
    rule4.tf = True
    rule4.num = 4
    rule4.name = 'macd大于前一天'

    rule5 = rule()
    rule5.tf = False
    rule5.num = 5
    rule5.name = '下影线'

    rule6 = rule()
    rule6.tf = False
    rule6.num = 6
    rule6.name = '蓝柱体'

    rule7 = rule()
    rule7.tf = True
    rule7.num = 7
    rule7.name = 'rsi'

    rule8 = rule()
    rule8.tf = True
    rule8.num = 8
    rule8.name = '5日线上交叉60日线'
    rule9 = rule()
    rule9.tf = True
    rule9.num = 9
    rule9.name = '5日线下交叉60日线'

    rule10 = rule()
    rule10.tf = True
    rule10.num = 10
    rule10.name = '有30日线'

    rule11 = rule()
    rule11.tf = False
    rule11.num = 11
    rule11.name = '5日线大于前一天'

    rule12 = rule()
    rule12.tf = True
    rule12.num = 12
    rule12.name = 'kdj金叉'

    rule13 = rule()
    rule13.tf = True
    rule13.num = 13
    rule13.name = 'jdk死叉'

    rule14 = rule()
    rule14.tf = True
    rule14.num = 14
    rule14.name = 'rsi金叉'

    rule15 = rule()
    rule15.tf = True
    rule15.num = 15
    rule15.name = 'rsi死叉'

    rule16 = rule()
    rule16.tf = True
    rule16.num = 16
    rule16.name = 'rsi小于某值'

    rule17 = rule()
    rule17.tf = True
    rule17.num = 17
    rule17.name = '低开'

    ruleList = []

    # 只把需要的规则加入rulelist中
    for num in allList:
        ruleList.append(locals()['rule' + str(num)])

    return ruleList


# 判断是否标记
def isChooseRule(ruleNum, list):
    ruleNum[0] = ruleNum[0] + 1
    if (ruleNum[0] in list):
        return True
    else:
        return False


# 给可选规则增加标记
def use_the_choose_rule(df, list):
    ruleId = [0]
    '''
    规则1:日线小于30日线的80%
    '''
    if (isChooseRule(ruleId, list)):
        df['日线小于30日线的75%'] = (df['close'] / df['60days'] <0.70)

    '''
    规则2:kdj小于20
    '''
    if (isChooseRule(ruleId, list)):
        # df['kdj小于20'] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
        # df['日线小于30日线的80%'] = (df['close'] / df['30days'] <0.8)
        # if (isChooseRule(ruleId, list)):
            # df['kdj小于20'] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
            # df['日线小于30日线的80%'] = (df['close'] / df['30days'] <0.8)
        df['日线小于30日线的80%'] = (df['kdj_k'] <= df['kdj_k'].shift()) & (df['kdj_k'].shift() <= df['kdj_k'].shift(2)) & (
            df['kdj_k'].shift(2) <=df['kdj_k'].shift(3)) & (df['kdj_k'].shift(3) <= df['kdj_k'].shift(4)) & (
                df['kdj_k'].shift(4) <= df['kdj_k'].shift(5))

    '''
    规则3:j大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['j大于前一天'] = (df['kdj_j'] > df['kdj_j'].shift()) & (df['kdj_k'] > df['kdj_k'].shift()) & (df['kdj_d'] > df['kdj_d'].shift())

    '''
    规则4:macd大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['macd大于前一天'] = df['macd'] > df['macd'].shift()

    '''
    规则5:下影线
    # 当日最低价：开盘价，跌幅大于3%。当日最低价：收盘价，跌幅大于3%
    # 收盘价：开盘价=99%-101%（涨跌幅1%以内）
    '''
    if (isChooseRule(ruleId, list)):
        df['下影线'] = (1 - (df['low'] / df['open']) > 0.03) & (1 - (df['low'] / df['close']) > 0.03) & (
            df['close'] / df['open'] > 0.99) & (df['close'] / df['open'] < 1.01)

    '''
    规则6:蓝柱体
    前日收盘价小于开盘价。前日收盘价：最低价，幅度在0.5%以内。当日收盘价大于开盘价
    '''
    if (isChooseRule(ruleId, list)):
        df['蓝柱体'] = (df['close'].shift() < df['open'].shift()) & (
            (df['close'].shift() / df['open'].shift()) - (df['low'].shift() / df['open'].shift()) <= 0.05) & (
                        df['close'] > df['open'])
    '''
    规则7:rsi
    RSI均小于 45。RSI均当日大于前日
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi'] = (df['rsi6'] < 45) & (df['rsi12'] < 45) & (df['rsi24'] < 45) & (df['rsi6'] > df['rsi6'].shift()) & (
            df['rsi12'] > df['rsi12'].shift()) & (
                        df['rsi24'] > df['rsi24'].shift())
    '''
    规则8
    5日线上交叉60日线
    '''
    if (isChooseRule(ruleId, list)):
        df['5日线上交叉60日线'] = (df['5days'].shift() < df['60days'].shift()) & (df['5days'] >= df['60days'])

    '''
    规则9
    5日线下交叉60日线
    '''
    if (isChooseRule(ruleId, list)):
        df['5日线下交叉60日线'] = (df['5days'].shift() > df['60days'].shift()) & (df['5days'] <= df['60days'])

    '''
    规则10
    有30日线
    '''
    if (isChooseRule(ruleId, list)):
        df['有30日线'] = df['30days'] > 0

    '''
    规则 11
    5日线上交叉60日线
    '''
    if (isChooseRule(ruleId, list)):
        df['5日线大于前一天'] = df['5days'] > df['5days'].shift()

    '''
    规则 12
    kdj金叉
    '''
    if (isChooseRule(ruleId, list)):
        df['kdj金叉'] = (df['kdj_j'].shift() < df['kdj_k'].shift()) & (df['kdj_j'] >= df['kdj_k'])

    '''
    规则 13
    jdk死叉
    '''
    if (isChooseRule(ruleId, list)):
        df['jdk死叉'] = (df['kdj_j'].shift() > df['kdj_k'].shift()) & (df['kdj_j'] <= df['kdj_k'])

    '''
    规则 14
    rsi金叉
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi金叉'] = (df['rsi6'].shift() < df['rsi24'].shift()) & (df['rsi6'] >= df['rsi24'])

    '''
    规则 15
    rsi死叉
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi死叉'] = (df['rsi6'].shift() > df['rsi24'].shift()) & (df['rsi6'] <= df['rsi24'])

    '''
    规则16:rsi小于40
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi小于某值'] = (df['rsi6'] < 40) & (df['rsi12'] < 40) & (df['rsi24'] < 40)

    '''
    规则17:低开
    '''
    if (isChooseRule(ruleId, list)):
        df['低开'] = df['open']/df['close'].shift()<0.95

    return df

'''
一规则法
每次只使用一个规则
'''


def all_rule(mustList):
    '''
    规则配置准备区,4,5,6,7,11,17
    '''
    ruleNumList = [1]
    ruleNumListMust = [10,4,7]
    # ruleNumList = [10]
    # ruleNumListMust = mustList

    totalCsvName = '60days'
    # 生存总规则list并且排序
    allList = ruleNumList + ruleNumListMust
    allList.sort()

    # 创建 规则号 的组合
    listAll = []
    for i in range(1, len(ruleNumList) + 1):
        iter = itertools.combinations(ruleNumList, i)
        listAll.append(list(iter))

    # 加载所有规则
    ruleList = get_all_rule(allList)
    print(datetime.datetime.now())
    '''第一步 获取所有的stock数据命名放入内存中'''
    count = 0
    # 1.读取base文件获取所有的csv文件名=code
    allCode = bs.get_all_code()

    # 声明一个dfnamelist用于存储所有的 stock内存名称
    dfmList = []
    # 声明一个total存储最终的总报表
    total = pd.DataFrame()
    # 2.循环所有的csv文件
    for code in allCode.code:
        codeStr = str(code).zfill(6)
        count = count + 1
        print('开始准备' + codeStr + '的内存数据,当前的数量是' + str(count))
        stockdf = 'df' + codeStr
        dfmList.append(stockdf)
        # 3.读取本地csv数据
        locals()[stockdf] = pd.read_csv(con.csvPath + codeStr + '.csv')

        '''第二步 当前stock增加规则标记'''
        locals()[stockdf] = use_the_choose_rule(locals()[stockdf], allList)
    dfmcount = 0
    exampleCount = 0
    '''第三步 循环执行所有的规则'''
    for inList in listAll:
        for brackets in inList:
            brackets = list(brackets) + ruleNumListMust
            brackets.sort()
            detailTempList = []
            # 1.基于规则循环所有stock内存数据 计算detail
            dfName = 'rule'
            for ruleNum in brackets:
                for rule in ruleList:
                    if (ruleNum == rule.num):
                        if (rule.tf == True):
                            dfName = dfName + '+' + str(ruleNum)
                        if (rule.tf == False):
                            dfName = dfName + '-' + str(ruleNum)
            exampleCount = exampleCount + 1
            print('开始生成规则' + dfName + '的数据!当前是第' + str(exampleCount) + '种规则.')
            print(datetime.datetime.now())
            for dfm in dfmList:
                dfc = copy.deepcopy(locals()[dfm])
                for ruleNum in brackets:
                    for rule in ruleList:
                        if (ruleNum == rule.num):
                            if (rule.tf == True):
                                dfc = dfc[dfc[rule.name] == True]
                            if (rule.tf == False):
                                dfc = dfc[dfc[rule.name] == False]
                if dfc.empty:
                    continue
                detailTempList.append(dfc)
            # 如果规则筛选出了样本则进行生成csv等
            if (len(detailTempList) > 0):
                tempDetail = pd.concat(detailTempList)
                if (False):
                    tempDetail = tempDetail[tempDetail['date'] > '2017-05-01']
                    if len(tempDetail) <= 0:
                        return -1
                if (True):
                    tempDetail.to_csv(con.detailPath + str(datetime.datetime.now().date()) + dfName + 'detail.csv',
                                      index=False)
                dft = view.get_total_csv(tempDetail, dfName)
                del tempDetail
                gc.collect()
                total = total.append(dft)
    print('生成totalcsv文件开始!' + str(datetime.datetime.now()))
    total.to_csv(con.detailPath + str(datetime.datetime.now().date()) + 'total' + totalCsvName + '.csv', index=False)
    print('生成csv文件结束!       ' + str(datetime.datetime.now()))
    return 1
all_rule(1)