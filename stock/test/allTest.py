from rule import rule
from common import constant as con
from calculate import calculate as cal
import tushare as ts
import pandas as pd
import numpy as np
import itertools
import copy
from base import baseStock as bs
import time


# 读取单一csv做测试
#
# def testforBuy():
#     stock_data = pd.read_csv(con.basePath + 'detail.csv')
#     for num in range(148):
#         if (num == 0):
#             continue
#         int = 1
#         count = 0
#         for data in stock_data.day2closeIncome:
#             count = count + 1
#             if ((num - 1) * 100 < count < num * 100):
#                 int = int * (data / 100 + 1)
#                 # print(str(num)+'组的收益为'+str(int))
#         print(str(int))
#
#
# def testIncome():
#     stock_data = pd.read_csv(con.csvPath + '603999.csv')
#     # 添加30日线
#     stock_data = cal.get_date_line(stock_data)
#     # 添加收益
#     stock_data = cal.get_income(stock_data)
#     # 输出到csv
#     stock_data.to_csv(con.csvPath + '603999new.csv', index=False)
#
#
# def testSigalCsv():
#     stock_data = pd.read_csv(con.csvPath + '603999.csv')
#     for day in [1, 2, 3, 4, 5, 6, 7]:
#         stock_data['day1open'] = stock_data['open'].shift(-1)
#         stock_data['day' + str(day)] = stock_data['date'].shift(-day)
#         # 基准开盘价=第一天开盘价
#         stock_data['day' + str(day) + 'income'] = round(stock_data['high'].shift(-day) / stock_data['day1open'],
#                                                         3) * 100 - 100
#         stock_data.to_csv(con.csvPath + '603999.csv', index=False)
#
#
# def test30Days():
#     stock_data = pd.read_csv(con.basePath + 'test.csv')
#     stock_data['30days'] = round(pd.rolling_mean(stock_data['close'], 30), 2)
#
#
# def testCombo():
#     df = pd.read_csv(con.csvPath + '603999.csv')
#
#     class rule:
#         num = 0
#         name = ''
#         formula = ''
#
#     ruleList = []
#     rule1 = rule()
#
#     rule1.num = 1
#     rule1.name = 'jdk小于20'
#     rule1.formula = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
#     rule2 = rule()
#     rule2.num = 2
#     rule2.name = 'jdk大于80'
#     rule2.formula = (df['kdj_k'] > 0) & (df['kdj_d'] > 0) & (df['kdj_j'] > 0)
#
#     ruleList.append(rule1)
#     ruleList.append(rule2)
#     ruleNumList = [1, 2]
#     listAll = []
#     for i in range(1, len(ruleNumList) + 1):
#         iter = itertools.combinations(ruleNumList, i)
#         listAll.append(list(iter))
#     for inList in listAll:
#         for brackets in inList:
#             for ruleNum in brackets:
#                 for rule in ruleList:
#                     ruleCsvName = ''
#                     if (ruleNum == rule.num):
#                         ruleCsvName = ruleCsvName.__add__(rule.name)
#                         df[rule.name] = rule.formula
#                         df = df[df[rule.name] == True]
#             # 输出到csv
#             df.to_csv(con.csvPath + ruleCsvName + '.csv', index=False)
#
#
# def testLocals():
#     # 创建 规则号 的组合
#     ruleNumList = [1, 2]
#     listAll = []
#     for i in range(1, len(ruleNumList) + 1):
#         iter = itertools.combinations(ruleNumList, i)
#         listAll.append(list(iter))
#
#     # 根据 规则号组合 声明最终转化csv的变量
#     for inList in listAll:
#         for brackets in inList:
#             dfName = 'rule'
#             for ruleNum in brackets:
#                 dfName = dfName + str(ruleNum) + '+'
#             locals()[dfName] = pd.DataFrame()
#
#     # 读取原始csv文件
#     df = pd.read_csv(con.csvPath + '603999.csv')
#
#     # 根据原始csv文件生成筛选 true False
#     class rule:
#         num = 0
#         name = ''
#         formula = ''
#
#     ruleList = []
#     rule1 = rule()
#     rule1.num = 1
#     rule1.name = 'jdk小于20'
#     df[rule1.name] = (df['kdj_k'] < 20) & (df['kdj_d'] < 20) & (df['kdj_j'] < 20)
#
#     rule2 = rule()
#     rule2.num = 2
#     rule2.name = 'jdk大于0'
#     df[rule2.name] = (df['kdj_k'] > 0) & (df['kdj_d'] > 0) & (df['kdj_j'] > 0)
#
#     ruleList.append(rule1)
#     ruleList.append(rule2)
#
#     for inList in listAll:
#         for brackets in inList:
#             dfc = copy.deepcopy(df)
#             dfName = 'rule'
#             for ruleNum in brackets:
#                 dfName = dfName + str(ruleNum) + '+'
#                 for rule in ruleList:
#                     if (ruleNum == rule.num):
#                         dfc = dfc[dfc[rule.name] == True]
#             if dfc.empty:
#                 continue
#             locals()[dfName] = locals()[dfName].append(dfc)
#
#     for inList in listAll:
#         for brackets in inList:
#             dfName = 'rule'
#             for ruleNum in brackets:
#                 dfName = dfName + str(ruleNum) + '+'
#             locals()[dfName].to_csv(dfName + '.csv')
#
#
# def test_append():
#     count = 0
#     allCode = bs.get_all_code()
#     # rightStock = pd.DataFrame()
#     dfList = []
#     for code in allCode.code:
#         codeStr = str(code).zfill(6)
#         print('开始筛选' + codeStr + '已经筛选了' + str(count))
#         stock_data = pd.read_csv(con.csvPath + codeStr + '.csv')
#         count = count + 1
#         dfList.append(stock_data)
#         # if (count > 2):
#         #     break
#     print('合并开始' + time.ctime())
#     rightStock = pd.concat(dfList)
#     print('合并结束' + time.ctime())
#     print(len(rightStock))
#     df2010 = rightStock[(rightStock['date'] < '2010/12/31')]
#     df2010 = df2010[(df2010['date'] > '2009/12/31')]
#     df2011 = rightStock[(rightStock['date'] < '2011/12/31')]
#     df2011 = df2011[(df2011['date'] > '2010/12/31')]
#     df2012 = rightStock[(rightStock['date'] < '2012/12/31')]
#     df2012 = df2012[(df2012['date'] > '2011/12/31')]
#     df2013 = rightStock[(rightStock['date'] < '2013/12/31')]
#     df2013 = df2013[(df2013['date'] > '2012/12/31')]
#     df2014 = rightStock[(rightStock['date'] < '2014/12/31')]
#     df2014 = df2014[(df2014['date'] > '2013/12/31')]
#     df2015 = rightStock[(rightStock['date'] < '2015/12/31')]
#     df2015 = df2015[(df2015['date'] > '2014/12/31')]
#     df2016 = rightStock[(rightStock['date'] < '2016/12/31')]
#     df2016 = df2016[(df2016['date'] > '2015/12/31')]
#     print(len(df2010))
#     print(len(df2011))
#     print(len(df2012))
#     print(len(df2013))
#     print(len(df2014))
#     print(len(df2015))
#     print(len(df2016))
#     df2010.to_csv('2010.csv')
#     df2011.to_csv('2011.csv')
#     df2012.to_csv('2012.csv')
#     df2013.to_csv('2013.csv')
#     df2014.to_csv('2014.csv')
#     df2015.to_csv('2015.csv')
#     df2016.to_csv('2016.csv')
#     return rightStock
#
#
# def test_mean():
#     count = 0
#     allCode = bs.get_all_code()
#     listMean = []
#     for code in allCode.code:
#         codeStr = str(code).zfill(6)
#         print('开始筛选' + codeStr + '已经筛选了' + str(count))
#         stock_data = pd.read_csv(con.csvPath + codeStr + '.csv')
#         count = count + 1
#         if(len(stock_data)>0):
#             stock_data = stock_data.sum()
#             listMean.append(stock_data.close / stock_data.open)
#     print(sum(listMean)/len(listMean))

def testArray():
    numlist = [1,2,3,4,5,6,7,8,9,11,12]
    listAll = []
    count = 0
    for i in range(1, len(numlist) + 1):
        iter = itertools.combinations(numlist, i)
        listAll.append(list(iter))
    for inList in listAll:
        # 2.循环规则数组中的每一个,
        for brackets in inList:
            count = count + 1
            print(count)

