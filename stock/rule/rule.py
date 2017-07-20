from base import baseStock as bs
import pandas as pd
from common import constant as con
from common import commonUtil
import copy
from view import view
from common import dateUtil

'''
获取成熟规则list,由于代码结构调整暂不可用,有需求时修改恢复
'''


# def get_total_list():
#     allList = []
#     df = pd.read_csv(con.detailPath + '2017-03-23total模拟开始纪念版数据收益.csv')
#     ruleLists = df['rule']
#     count = 0
#     for ruleList in ruleLists:
#         count = count + 1
#         ruleList = ruleList.replace('rule', '')
#         ruleList = ruleList.replace('+10', '')
#         ruleList = ruleList.replace('+', ',')
#         ruleList = ruleList.replace('-', ',')
#         ruleList = ruleList.replace(',', '', 1)
#         list(ruleList)
#         tempList = ruleList.split(',')
#         rightList = []
#         for rule in tempList:
#             ruleInt = int(rule)
#             rightList.append(ruleInt)
#         allList.append(rightList)
#     return allList

def get_all_index_rule(allList):
    class rule:
        num = 0
        name = ''

    rule10001 = rule()
    rule10001.tf = True
    rule10001.num = 10001
    rule10001.name = '日线小于30日线的75%'
    ruleList = []
    # 只把需要的规则加入rulelist中
    for num in allList:
        ruleList.append(locals()['rule' + str(num)])
    return ruleList

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

    rule18 = rule()
    rule18.tf = True
    rule18.num = 18
    rule18.name = '交易量猛增'

    rule19 = rule()
    rule19.tf = True
    rule19.num = 19
    rule19.name = '收盘价大于前一天'

    rule20 = rule()
    rule20.tf = True
    rule20.num = 20
    rule20.name = '日线大于前一天'

    rule21 = rule()
    rule21.tf = True
    rule21.num = 21
    rule21.name = '日线成多头排列'

    rule22 = rule()
    rule22.tf = True
    rule22.num = 22
    rule22.name = '日线紧密排列'

    '''
    以下为大盘规则
    '''
    rule10001 = rule()
    rule10001.tf = True
    rule10001.num = 10001
    rule10001.name = '大盘规则1'
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
'''
根据股票代码,获取对应的指数缓存
'''
def get_right_indexCash(codeStr):
    indexCashName = 'indexCash'
    if(con.shenIndexBegin == codeStr):
        indexCashName = indexCashName+con.shenIndex
    if(con.chuangIndexBegin == codeStr):
        indexCashName = indexCashName+con.chuangIndex
    if(con.shangIndexBegin == codeStr):
        indexCashName = indexCashName+con.shangIndex
    if(con.shangBIndexBegin == codeStr):
        indexCashName = indexCashName+con.shangIndex
    dfIndex = globals()[indexCashName]
    return dfIndex

def use_the_index_choose_rule(dfIndex, list):
    ruleId = [10000]
    '''
    规则10001:大盘规则1
    '''
    if (isChooseRule(ruleId, list)):
        dfIndex['大盘规则1'] = dfIndex['macd'] > dfIndex['macd'].shift()
    return dfIndex

'''
给stock增加技术指标标记
'''


def use_the_choose_rule(df, list):
    ruleId = [0]

    '''
    规则1:日线小于30日线的80%
    '''
    if (isChooseRule(ruleId, list)):
        df['日线小于30日线的75%'] = (df['2days'] / df['60days'] < 0.74) & (df['close'] / df['30days'] < 0.82)

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
            df['kdj_k'].shift(2) <= df['kdj_k'].shift(3)) & (df['kdj_k'].shift(3) <= df['kdj_k'].shift(4)) & (
                                 df['kdj_k'].shift(4) <= df['kdj_k'].shift(5))

    '''
    规则3:j大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['j大于前一天'] = (df['kdj_j'] > df['kdj_j'].shift()) & (df['kdj_k'] > df['kdj_k'].shift()) & (
            df['kdj_d'] > df['kdj_d'].shift())

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
    RSI均小于 45且大于30。RSI均当日大于前日
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi'] = (df['rsi6'] < 45) & (df['rsi12'] < 45) & (df['rsi24'] < 45) & (df['rsi6'] > df['rsi6'].shift()) & (
            df['rsi12'] > df['rsi12'].shift()) & (df['rsi24'] > df['rsi24'].shift()) & (df['rsi6'] > 30) & (
                        df['rsi12'] > 30) & (df['rsi24'] > 30)
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
        df['低开'] = df['open'] / df['close'].shift() < 0.95

    '''
    规则18:交易量猛增
    '''
    if (isChooseRule(ruleId, list)):
        df['交易量猛增'] = df['volume'] / df['volume'].shift() > 3

    '''
    规则19：收盘价大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['收盘价大于前一天'] = (df['close'] > df['close'].shift())

    '''
    规则20：日线大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['日线大于前一天'] = (df['5days'] > df['5days'].shift()) & (df['10days'] > df['10days'].shift()) & (
        df['20days'] > df['20days'].shift()) & (df['30days'] > df['30days'].shift())

    '''
    规则21：日线成多头排列
    '''
    if (isChooseRule(ruleId, list)):
        df['日线成多头排列'] = (df['5days'] > df['10days']) & (df['10days'] > df['20days']) & (df['20days'] > df['30days'])

    '''
    规则22：日线紧密排列
    '''
    if (isChooseRule(ruleId, list)):
        df['日线紧密排列'] = (df['5days']/df['10days']<1.005) & (df['10days']/df['20days']<1.005) & (df['20days']/df['30days']<1.005)
    return df

'''
增加股票规则标记
'''


def add_stock_mark(stockCashList, allList):
    for stockCash in stockCashList:
        globals()[stockCash] = use_the_choose_rule(globals()[stockCash], allList)

        '''
        对股票做大盘指数规则附加
        '''
        #获取股票代码的前两位
        stockCode = stockCash[9:11]
        dfIndex = get_right_indexCash(stockCode)
        globals()[stockCash] = pd.merge(globals()[stockCash], dfIndex, how='left', on=['date'])

'''
开始生成符合规则的股票数据,根据股票标记与规则一一对应筛选
'''


def get_TF_stock(stockCashList, brackets, ruleList):
    # 为了存储 筛选出的股票组成detail 声明一个数组
    detailTempList = []
    # 5.循环所有的缓存csv列表,处理缓存数据
    for dfm in stockCashList:
        # 复制一份缓存数据,以免影响后面的规则
        dfc = copy.deepcopy(globals()[dfm])
        # 6.根据规则列表中规则是ture还是false来筛选符合情况的股票
        for ruleNum in brackets:
            for rule in ruleList:
                if (ruleNum == rule.num):
                    # 如果规则是True则股票数据使用True筛选
                    if (rule.tf == True):
                        dfc = dfc[dfc[rule.name] == True]
                    # 如果规则是False则股票数据使用False筛选
                    if (rule.tf == False):
                        dfc = dfc[dfc[rule.name] == False]
        # 如果筛选后,没有任何股票符合条件,则直接跳过此规则
        if dfc.empty:
            continue
        # 7.将符合条件的股票加入临时变量集合中
        detailTempList.append(dfc)
    return detailTempList


'''
循环规则组合与股票标记一一对应 生成detail和total报表
'''


def generate_report_form(ChooseCombinations, ruleNumListMust, ruleList, stockCashList, stockArgX):
    # 声明最终的total报表
    totalReportForm = pd.DataFrame()

    # 规则实例数量
    exampleCount = 0
    # 1.循环所有的规则数组组合
    for inList in ChooseCombinations:
        # 2.循环规则数组中的每一个,
        for brackets in inList:
            # 将必选规则添加到规则中
            brackets = list(brackets) + ruleNumListMust
            # 对形成的规则排序
            brackets.sort()
            # 为规则前面加rule前缀
            ruleName = 'rule'
            # 3.循环每一个数组中的每一个规则
            for ruleNum in brackets:
                # 4.循环规则列表中的每一个规则属性和数组中的规则匹配,来生成规则命名
                for rule in ruleList:
                    if (ruleNum == rule.num):
                        # 如果规则定义为Ture增加+号标记
                        if (rule.tf == True):
                            ruleName = ruleName + '+' + str(ruleNum)
                        # 如果规则定义为Ture增加-号标记
                        if (rule.tf == False):
                            ruleName = ruleName + '-' + str(ruleNum)
            # 规则实例数量+1
            exampleCount = exampleCount + 1
            print('开始生成规则' + ruleName + '的数据!当前是第' + str(exampleCount) + '种规则.')
            # 打印当前时间
            dateUtil.print_date()

            '''
            开始生成复合规则的股票数据,根据股票标记与规则一一对应筛选
            '''
            detailTempList = get_TF_stock(stockCashList, brackets, ruleList)

            '''
            开始生成detail.csv报表
            '''
            tempDetail = view.generate_detail_csv(detailTempList, stockArgX, ruleName)

            '''
            开始生成某规则的收益total数据
            '''
            totalProfit = view.get_total_csv(tempDetail, ruleName, stockArgX)
            # 将某规则的收益total数据添加到total报表中
            totalReportForm = totalReportForm.append(totalProfit)

    print('生成totalcsv文件开始!')
    dateUtil.print_date()
    # 最终生成csv命名
    totalCsvName = stockArgX.totalCsvName
    totalReportForm.to_csv(con.detailPath + str(
        dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + 'total' + totalCsvName + '.csv',
                           index=False)
    print('生成csv文件结束!')


'''
获取所有的stock数据命名放入内存中
'''


def put_all_stock_into_cash(baseCodeList):
    count = 0
    # 声明一个dfnamelist用于存储所有的 stock内存名称
    stockCashList = []
    # 2.循环所有的csv文件
    for codeStr in baseCodeList:
        count = count + 1
        print('开始准备' + codeStr + '的内存数据,当前的数量是' + str(count))
        stockCash = 'stockCash' + codeStr
        stockCashList.append(stockCash)
        # 3.读取本地csv数据
        globals()[stockCash] = pd.read_csv(con.csvPath + codeStr + '.csv')
    return stockCashList


'''
获取所有的stock数据命名放入内存中
'''


def put_all_index_into_cash():
    baseIndexList = con.baseIndexList
    count = 0
    # 声明一个dfnamelist用于存储所有的 stock内存名称
    indexCashList = []
    # 2.循环所有的csv文件
    for codeStr in baseIndexList:
        count = count + 1
        print('开始准备' + codeStr + '的指数内存数据,当前的数量是' + str(count))
        indexCash = 'indexCash' + codeStr
        indexCashList.append(indexCash)
        # 3.读取本地csv数据放入全局变量中
        globals()[indexCash] = pd.read_csv(con.indexCsvPath + codeStr + '.csv')
    return indexCashList
'''
为每一个指数基础数据增加规则TF标记后,去掉基础数据
'''
def add_ruleTF_for_index(indexCashList,allList):
    for indexCash in indexCashList:
        globals()[indexCash] = use_the_index_choose_rule(globals()[indexCash],allList)
        globals()[indexCash] = globals()[indexCash].drop(con.allBaseNameOrder,axis=1)




'''
按规则参数生成股票数据
'''


def make_stockData_by_choose(stockArgX):
    ruleNumListChoose = stockArgX.ruleNumListChoose
    ruleNumListMust = stockArgX.ruleNumListMust
    '''
    1.1 创建 股票可选规则 的所有组合
    '''
    ChooseCombinations = commonUtil.get_all_combinations(ruleNumListChoose)


    '''
    2.1 加载股票 输入规则集合的属性信息
    '''
    # 生成 可选和必选规则的 集合list
    allList = ruleNumListChoose + ruleNumListMust
    # 对集合list排序
    allList.sort()
    # 根据集合list加载需要的规则对象
    ruleList = get_all_rule(allList)

    '''
    3.获取base.csv中所有的code
    '''
    baseCodeList = bs.put_base_csv_code_into_cash()

    '''
    4.1获取所有的stock数据命名放入内存中,返回stock内存数据名称list
    '''
    stockCashList = put_all_stock_into_cash(baseCodeList)
    '''
    4.2获取所有的index数据放入内存中
    '''
    indexCashList = put_all_index_into_cash()
    '''
    4.3为所有指数增加规则TRUE FALSE
    '''
    add_ruleTF_for_index(indexCashList,allList)


    '''
    5.1 为当前所有stock增加股票规则标记
    '''
    add_stock_mark(stockCashList, allList)


    '''
    6.循环规则组合与股票标记一一对应 生成detail和total报表
    '''
    generate_report_form(ChooseCombinations, ruleNumListMust, ruleList, stockCashList, stockArgX)
