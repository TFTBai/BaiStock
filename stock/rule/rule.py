from base import baseStock as bs
import pandas as pd
from common import constant as con
from common import commonUtil
from view import view
from common import dateUtil
from simulation import simulation
from calculate import calculate as cal
from common import mailUtil

def get_rules_df(stockArgX):
    '''
    获取成熟规则列表
    '''
    df = pd.read_csv(con.rulesPath + stockArgX.mustByCsvName+'.csv')
    return df

def get_all_rule(allList):
    class rule:
        num = 0
        name = ''

    rule1 = rule()
    rule1.tf = True
    rule1.value = False
    rule1.num = 1
    rule1.name = '日线小于30日线的75%'

    rule2 = rule()
    rule2.tf = True
    rule2.value = False
    rule2.num = 2
    rule2.name = '日线小于30日线的80%'

    rule3 = rule()
    rule3.tf = True
    rule3.value = False
    rule3.num = 3
    rule3.name = 'j大于前一天'

    rule4 = rule()
    rule4.tf = True
    rule4.value = False
    rule4.num = 4
    rule4.name = 'macd大于前一天'

    rule5 = rule()
    rule5.tf = True
    rule5.value = False
    rule5.num = 5
    rule5.name = '下影线'

    rule6 = rule()
    rule6.tf = True
    rule6.value = False
    rule6.num = 6
    rule6.name = '蓝柱体'

    rule7 = rule()
    rule7.tf = True
    rule7.value = False
    rule7.num = 7
    rule7.name = 'rsi'

    rule8 = rule()
    rule8.tf = True
    rule8.value = False
    rule8.num = 8
    rule8.name = '5日线上交叉60日线'

    rule9 = rule()
    rule9.tf = True
    rule9.value = False
    rule9.num = 9
    rule9.name = '5日线下交叉60日线'

    rule10 = rule()
    rule10.tf = True
    rule10.value = False
    rule10.num = 10
    rule10.name = '有30日线'

    rule11 = rule()
    rule11.tf = True
    rule11.value = False
    rule11.num = 11
    rule11.name = '5日线大于前一天'

    rule12 = rule()
    rule12.tf = True
    rule12.value = False
    rule12.num = 12
    rule12.name = 'kdj金叉'

    rule13 = rule()
    rule13.tf = True
    rule13.value = False
    rule13.num = 13
    rule13.name = 'jdk死叉'

    rule14 = rule()
    rule14.tf = True
    rule14.value = False
    rule14.num = 14
    rule14.name = 'rsi金叉'

    rule15 = rule()
    rule15.tf = True
    rule15.value = False
    rule15.num = 15
    rule15.name = 'rsi死叉'

    rule16 = rule()
    rule16.tf = True
    rule16.value = False
    rule16.num = 16
    rule16.name = 'rsi小于某值'

    rule17 = rule()
    rule17.tf = True
    rule17.value = False
    rule17.num = 17
    rule17.name = '低开'

    rule18 = rule()
    rule18.tf = True
    rule18.value = False
    rule18.num = 18
    rule18.name = '交易量猛增'

    rule19 = rule()
    rule19.tf = True
    rule19.value = False
    rule19.num = 19
    rule19.name = '收盘价大于前一天'

    rule20 = rule()
    rule20.tf = True
    rule20.value = False
    rule20.num = 20
    rule20.name = '日线大于前一天'

    rule21 = rule()
    rule21.tf = True
    rule21.value = False
    rule21.num = 21
    rule21.name = '日线成多头排列'

    rule22 = rule()
    rule22.tf = True
    rule22.value = False
    rule22.num = 22
    rule22.name = '日线紧密排列'

    rule23 = rule()
    rule23.tf = True
    rule23.value = True
    rule23.num = 23
    rule23.name = '20天后收益'

    '''
    以下为大盘规则
    '''
    rule10001 = rule()
    rule10001.tf = True
    rule10001.value = False
    rule10001.num = 10001
    rule10001.name = '大盘规则1'

    rule10002 = rule()
    rule10002.tf = True
    rule10002.value = False
    rule10002.num = 10002
    rule10002.name = '大盘规则2'

    rule10003 = rule()
    rule10003.tf = True
    rule10003.value = False
    rule10003.num = 10003
    rule10003.name = '大盘规则3'
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
    if (con.shenIndexBegin == codeStr):
        indexCashName = indexCashName + con.shenIndex
    if (con.chuangIndexBegin == codeStr):
        indexCashName = indexCashName + con.chuangIndex
    if (con.shangIndexBegin == codeStr):
        indexCashName = indexCashName + con.shangIndex
    if (con.shangBIndexBegin == codeStr):
        indexCashName = indexCashName + con.shangIndex
    dfIndex = globals()[indexCashName]
    return dfIndex


def use_the_index_choose_rule(dfIndex, list):
    ruleId = [10000]
    '''
    规则10001:大盘规则1
    '''
    if (isChooseRule(ruleId, list)):
        dfIndex['大盘规则1'] = (dfIndex['close'] / dfIndex['close'].shift() < 0.995) & (
            dfIndex['close'].shift() / dfIndex['close'].shift(2) < 0.995)
    '''
    规则10002:大盘规则2
    '''
    if (isChooseRule(ruleId, list)):
        dfIndex['大盘规则2'] = (dfIndex['close'] / dfIndex['60days'] > 1.05)
    '''
    规则10003:大盘规则3
    '''
    if (isChooseRule(ruleId, list)):
        dfIndex['大盘规则3'] = (dfIndex['close'] / dfIndex['close'].shift() > 1.008) & (
            dfIndex['close'].shift() / dfIndex['close'].shift(2) > 1.008)
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
        df['日线小于30日线的75%'] = ((df['2days'] / df['60days'] < 0.74) & (df['close'] / df['30days'] < 0.82)) | (
            df['close'] / df['30days'] < 0.7) | (df['2days'] / df['60days'] < 0.64)

    '''
    规则2:kdj小于20
    '''
    if (isChooseRule(ruleId, list)):
        # df['kdj小于20'] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
        # df['日线小于30日线的80%'] = (df['close'] / df['30days'] <0.8)
        # if (isChooseRule(ruleId, list)):
        # df['kdj小于20'] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
        # df['日线小于30日线的80%'] = (df['close'] / df['30days'] <0.8)
        df['日线小于30日线的80%'] = (df['2days'] / df['60days'] < 0.79) & (df['close'] / df['30days'] < 0.86) & (
            df['2days'] / df['60days'] >= 0.74) & (df['close'] / df['30days'] >= 0.82)
    '''
    规则3:j大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['j大于前一天'] = (df['2days'] / df['60days'] < 0.84) & (df['close'] / df['30days'] < 0.9) & (
            df['2days'] / df['60days'] >= 0.79) & (df['close'] / df['30days'] >= 0.86)
    '''
    规则4:macd大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['macd大于前一天'] = (df['close'] / df['close'].shift(40) < 0.63) & (df['close'] / df['close'].shift(10) < 0.9)


    '''
    规则5:下影线
    # 当日最低价：开盘价，跌幅大于3%。当日最低价：收盘价，跌幅大于3%
    # 收盘价：开盘价=99%-101%（涨跌幅1%以内）
    '''
    if (isChooseRule(ruleId, list)):
        df['下影线'] = (df['close'] / df['close'].shift(40) < 0.71) & ((df['close'] / df['close'].shift(60) < 0.65) | (
            df['close'] / df['close'].shift(10) < 0.9))

    '''
    规则6:蓝柱体
    前日收盘价小于开盘价。前日收盘价：最低价，幅度在0.5%以内。当日收盘价大于开盘价
    '''
    if (isChooseRule(ruleId, list)):
        df['蓝柱体'] = (df['close'] / df['open'].shift(5) < 0.91) & (df['close'] / df['open'].shift(10) < 0.87) & (
            df['close'] / df['open'].shift(15) < 0.83) & (df['close'] / df['open'].shift(20) < 0.79) & (
            df['close'] / df['open'].shift(25) < 0.75) & (df['close'] / df['open'].shift(30) < 0.71)
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
        df['5日线上交叉60日线'] = (df['kdj_k'] > 20) & (df['kdj_d'] > 20) & (df['kdj_j'] > 20) & (df['kdj_j'] < 40) & (
            df['kdj_j'] < 40) & (df['kdj_j'] < 40)

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
        df['5日线大于前一天'] =(df['close'] / df['low'] < 1.07) & (df['close'] / df['low'] > 1.04)


    '''
    规则 12
    kdj金叉
    '''
    if (isChooseRule(ruleId, list)):
        df['kdj金叉'] = (df['close'] / df['close'].shift() < 0.95)

    '''
    规则 13
    jdk死叉
    '''
    if (isChooseRule(ruleId, list)):
        df['jdk死叉'] = (df['macd'] > df['macd'].shift()) & (
            df['close'] / df['close'].shift() > 1.02)

    '''
    规则 14
    rsi金叉
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi金叉'] = ((df['close'] / df['close'].shift()) >= (df['close'].shift() / df['close'].shift(2))) & ((
            df['close'].shift() / df['close'].shift(2)) >= (df['close'].shift(2) / df['close'].shift(3)))
    '''
    规则 15
    rsi死叉
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi死叉'] = (df['close'] / df['close'].shift() > 1.025) & (
        df['close'].shift() / df['close'].shift(2) > 1.025) & (
                       df['close'].shift(2) / df['close'].shift(3) > 1.025)

    '''
    规则16:rsi小于40
    '''
    if (isChooseRule(ruleId, list)):
        df['rsi小于某值'] = (df['2days'] / df['60days'] < 0.74) & (df['close'] / df['30days'] < 0.82) & (
            df['close'] / df['close'].shift() > 1.025)

    '''
    规则17:低开
    '''
    if (isChooseRule(ruleId, list)):
        df['低开'] = (df['close'] / df['close'].shift() > 1.055) & (
        df['close'].shift() / df['close'].shift(2) > 1.055) & (
                       df['close'].shift(2) / df['close'].shift(3) > 1.055)

    '''
    规则18:交易量猛增
    '''
    if (isChooseRule(ruleId, list)):
        df['交易量猛增'] = (df['open'] / df['high'] < 0.98) & (df['close'] / df['high'] < 0.98) & (
            df['open'].shift() / df['high'].shift() < 0.98) & (df['close'].shift() / df['high'].shift() < 0.98)

    '''
    规则19：收盘价大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['收盘价大于前一天'] = (df['volume'] / df['volume'].shift() < 1.3) & (df['volume'] / df['volume'].shift() > 0.7)

    '''
    规则20：日线大于前一天
    '''
    if (isChooseRule(ruleId, list)):
        df['日线大于前一天'] = (df['low'].shift(-1) / df['close'] < 1.095)

    '''
    规则21：日线成多头排列
    '''
    if (isChooseRule(ruleId, list)):
        df['日线成多头排列'] = (df['volume5days'] / df['volume30days'] < 0.95) & (
            df['volume10days'] / df['volume30days'] < 0.95) & (
            df['volume5days'] / df['volume10days'] < 0.95)

    '''
    规则22：日线紧密排列
    '''
    if (isChooseRule(ruleId, list)):
        df['日线紧密排列'] = (
            df['volume10days'] / df['volume30days'] < 0.95) & (
            df['volume5days'] / df['volume10days'] < 0.95)

    '''
    规则23:20天后收益
    '''
    if (isChooseRule(ruleId, list)):
        df['30天后收益'] = round(df['close'].shift(-31) / df['open'].shift(-1), 3)

    return df




def add_stock_mark(stockCashList, stockArgX):
    '''
    增加股票规则标记
    '''

    #如果使用成熟规则,则使用临时固定的  股票规则标记列表 //TODO 需要调整结构,自动根据表中的来
    if (stockArgX.mustByCsvTF == True):
        allList = stockArgX.mustByCsvRule
    else:
        allList = stockArgX.ruleNumListChoose + stockArgX.ruleNumListMust

    count = 0
    for stockCash in stockCashList:
        stockCashDataFrame = globals()[stockCash]
        count = count + 1
        print('开始为' + stockCash + '缓存增加规则TF,当前的数量是' + str(count))
        stockCashDataFrame = use_the_choose_rule(stockCashDataFrame, allList)
        if (stockArgX.indexOpen):
            '''
            对股票做大盘指数规则附加
            '''
            # 获取股票代码的前两位
            stockCode = stockCash[9:11]
            dfIndex = get_right_indexCash(stockCode)
            stockCashDataFrame = pd.merge(stockCashDataFrame, dfIndex, how='left', on=['date'])
        # 9.是否进行日期筛选
        if (stockArgX.dateBeginTF):
            stockCashDataFrame = stockCashDataFrame[stockCashDataFrame['date'] >= stockArgX.dateBeginRange]
        if (stockArgX.dateEndTF):
            stockCashDataFrame = stockCashDataFrame[stockCashDataFrame['date'] < stockArgX.dateEndRange]
        globals()[stockCash] = stockCashDataFrame



'''
开始生成符合规则的股票数据,根据股票标记与规则一一对应筛选
'''


def get_TF_stock(stockCashList, brackets, ruleList):
    # 为了存储 筛选出的股票组成detail 声明一个数组
    detailTempList = []
    # 5.循环所有的缓存csv列表,处理缓存数据
    for dfm in stockCashList:
        dfc = globals()[dfm]
        # 6.根据规则列表中规则是ture还是false来筛选符合情况的股票
        for ruleNum in brackets:
            for rule in ruleList:
                if (ruleNum == rule.num):
                    # 如果规则是True则股票数据使用True筛选
                    if (rule.tf == True):
                        if (rule.value == True):
                            continue
                        dfc = dfc[dfc[rule.name] == True]
                    # 如果规则是False则股票数据使用False筛选
                    if (rule.tf == False):
                        if (rule.value == True):
                            continue
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
            if (len(detailTempList) <= 0):
                continue
            '''
            开始生成detail.csv报表
            '''
            tempDetail = view.generate_detail_csv(detailTempList, stockArgX, ruleName)

            if (stockArgX.groupByDaysTF):
                '''
                开始生成某规则的收益total数据
                '''
                totalReportForm = view.get_total_csv_by_year(tempDetail, ruleName, stockArgX, totalReportForm)
            else:
                '''
                开始生成某规则的收益total数据
                '''
                totalProfit = view.get_total_csv(tempDetail, ruleName, stockArgX)

                '''
                开始按年生成某规则的收益total数据
                '''
                # 将某规则的收益total数据添加到total报表中
                totalReportForm = totalReportForm.append(totalProfit)

    if(len(totalReportForm)>0):
        print('筛选成功,生成totalcsv文件开始!')
        dateUtil.print_date()
        # 最终生成csv命名
        totalCsvName = stockArgX.totalCsvName
        totalReportForm.to_csv(con.detailPath + str(
            dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + 'total' + totalCsvName + '.csv',
                               index=False)
        print('生成csv文件结束!')
        stockArgX.TFHaveResult = True



def put_all_stock_into_cash(baseCodeList):
    '''
    获取所有的stock数据命名放入内存中
    '''
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


def add_ruleTF_for_index(indexCashList, allList):
    for indexCash in indexCashList:
        globals()[indexCash] = use_the_index_choose_rule(globals()[indexCash], allList)
        globals()[indexCash] = globals()[indexCash].drop(con.allBaseNameOrder, axis=1)

'''
增加策略买卖收益

整体思路如下
①读detail表，获取日期list
开始每日的循环
    ②根据日期 遍历每一个股票
    开始股票的循环
        ③根据股票，读取内存中的base csv数据
        ④根据base csv，和开始日期 锁定当日数据
        ⑤根据买入规则，模拟买入 （如果没符合买入规则，跳出循环）
        ⑥根据卖出规则，模拟卖出（如果最后一个交易日没卖出，强制卖出）
'''
def add_strategy_income(df,rightStockStrategy,stockArgX,dfname):
    #声明所有日期的总收益列表
    all_date_income_list = []
    #声明所有卖出day的列表
    all_sell_day_list = []
    #声明所有卖出day的列表
    all_sell_day_list_for_mean = []
    #①读detail表，获取日期list
    date_list = commonUtil.get_detail_date(rightStockStrategy)
    #循环每一个日期
    for date in date_list:
        #声明当前日期的收益list
        now_date_income_list = []
        #拿出对应日期的detail数据
        dateDetailStock = rightStockStrategy[rightStockStrategy['date']==date]
        code_list = dateDetailStock['code']
        #平均卖出天数list
        mean_sell_day_list = []
        #循环每一个股票
        for code in code_list:
            stockCashCode = 'stockCash'+ str(int(code)).zfill(6)
            baseStockInfo = globals()[stockCashCode]
            right_strategy = simulation.get_strategy_income(baseStockInfo,date,stockArgX)
            #如果策略买卖成功则加入 当前日期收益list
            if(right_strategy.sell_success ==True):
                #补偿算法 处理收益值
                now_date_income_list.append(cal.compensate_formula_for_int(right_strategy.strategy_income))
                #赋值卖出day
                all_sell_day_list.append(right_strategy.sell_day)
                mean_sell_day_list.append(right_strategy.sell_day)

        #如果当前日期 没有符合策略的股票则跳过
        if(len(now_date_income_list)==0):
            continue
        # 获取当前日期 平均收益
        strategy_income = commonUtil.get_mean_by_list(now_date_income_list)
        # 当前日期平均收益加入总收益列表
        all_date_income_list.append(strategy_income)

        if(len(mean_sell_day_list)>3):
            mean_sell_day_list = [commonUtil.get_mean_by_list(mean_sell_day_list)]
        all_sell_day_list_for_mean = all_sell_day_list_for_mean + mean_sell_day_list

    if(len(all_date_income_list) > 0):
        #将总策略收益列表 做平均
        strategy_income_mean = commonUtil.get_mean_by_list(all_date_income_list)
        #将总策略平均收益赋值到total表中
        df['策略收益'] = strategy_income_mean
        sell_day_list = con.get_day_list(stockArgX.cutMeatDay)
        for day in sell_day_list:
            dayName = 's'+str(day)
            df[dayName] = all_sell_day_list.count(day)
        df['平均卖出天数'] = commonUtil.get_mean_by_list(all_sell_day_list_for_mean)
    return df

'''
生成股票数据
'''
def make_stockData(stockArgX):

    '''
    1.获取base.csv中所有的code
    '''
    baseCodeList = bs.put_base_csv_code_into_cash(stockArgX)

    '''
    2获取所有的stock数据命名放入内存中,返回stock内存数据名称list
    '''
    stockCashList = put_all_stock_into_cash(baseCodeList)

    '''
    3 为当前所有stock增加股票规则标记
    '''
    add_stock_mark(stockCashList, stockArgX)

    '''
    4.执行某种模式的股票筛选
    '''
    make_stock_by_mode(stockCashList,stockArgX)
    '''
    5.发送邮件
    '''
    if(stockArgX.TFmail==True):
        make_stock_email(stockArgX)


def make_stock_by_mode(stockCashList,stockArgX):
    '''
    按照列表模式或者组合模式做筛选
    '''
    #如果使用成熟规则 则循环,否则只执行一次
    if(stockArgX.mustByCsvTF == True):
        stockArgX.ruleNumListChoose = [10]
        #获取成熟规则列表
        rulesDataframe = get_rules_df(stockArgX)
        for index in rulesDataframe.index:
            print("开始筛选的规则排名为==============" + str(index+1))
            #组装StockArgX
            assembleStockArgX(rulesDataframe,stockArgX,index)
            #按规则参数生成股票数据
            make_stockData_by_choose(stockArgX,stockCashList)
            if (stockArgX.TFHaveResult == True):
                print("已找到符合条件的stock 筛选程序运行完毕,开始获取detail信息! ")
                tempDetail = stockArgX.detail
                codeList = tempDetail['code'].tolist()
                for code in codeList:
                    #查询code对应的股票名称
                    base_df = bs.get_all_code()
                    base_df = base_df[base_df['code']==code]
                    codeName = base_df['name'].values[0]
                    codeInfo = stockArgX.codeInfo
                    codeInfo = codeInfo+ str(code).zfill(6)+' '+codeName+' '
                    stockArgX.codeInfo = codeInfo
                break
    else:
        #按规则参数生成股票数据
        make_stockData_by_choose(stockArgX,stockCashList)


def assembleStockArgX(rulesDataframe,stockArgX,index):
    '''组装StockArgX'''
    ranking = index + 1
    ruleName = rulesDataframe.loc[index].rule
    stockArgX.ranking = ranking
    stockArgX.ruleName = ruleName
    stockArgX.ruleExpectIncome = float(rulesDataframe.loc[index][5:20].sort_values(ascending=False)[0:1][0])
    stockArgX.ruleHoldDay = int(rulesDataframe.loc[index][20:34].sort_values(ascending=False)[0:1].index[0].replace('d','').replace('cZ',''))
    stockArgX.ruleExpectZ = float(rulesDataframe.loc[index][20:34].sort_values(ascending=False)[0:1][0])
    stockArgX.ruleDetailInfo = str(rulesDataframe.loc[index])
    #从ruleName中提取rule
    ruleName = ruleName.replace('rule', '')
    ruleName = ruleName.replace('+10', '')
    ruleName = ruleName.replace('+20', '')
    ruleName = ruleName.replace('+', ',')
    ruleName = ruleName.replace('-', ',')
    ruleName = ruleName.replace(',', '', 1)
    tempList = ruleName.split(',')
    rightRule = []
    for rule in tempList:
        ruleInt = int(rule)
        rightRule.append(ruleInt)
    stockArgX.ruleNumListMust = rightRule
    return stockArgX

'''
制作邮件内容并且发送
'''

def make_stock_email(stockArgX):
    title ='筛选结果:'+stockArgX.dateBeginRange
    msg = stockArgX.codeInfo +' '+'排名:'+str(stockArgX.ranking)+' '+'day'+str(stockArgX.ruleHoldDay) +' '\
          +'xxxxx卖\n'+'预期收益:'+str(stockArgX.ruleExpectIncome)+' '+'得分值:'+str(stockArgX.ruleExpectZ)+'\n'\
          +'筛选日期:'+stockArgX.dateBeginRange+'\n'\
          +'规则详细信息:\n'+str(stockArgX.ruleDetailInfo)
    mailUtil.sendEmail(title,msg)
    print(msg)

'''
按规则参数生成股票数据
'''
def make_stockData_by_choose(stockArgX,stockCashList):
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

    if(stockArgX.indexOpen ==True):
        '''
        4.2获取所有的index数据放入内存中
        '''
        indexCashList = put_all_index_into_cash()
        '''
        4.3为所有指数增加规则TRUE FALSE
        '''
        add_ruleTF_for_index(indexCashList, allList)

    '''
    6.循环规则组合与股票标记一一对应 生成detail和total报表
    '''
    generate_report_form(ChooseCombinations, ruleNumListMust, ruleList, stockCashList, stockArgX)
