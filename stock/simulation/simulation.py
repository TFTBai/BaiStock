import pandas as pd
from common import constant as con

'''
模拟操作类
整体思路如下

①读detail表，获取日期list
开始每日的循环
②根据日期 随机选一个作为买卖的股票
③根据选定的股票，读取内存中的base csv数据
④根据base csv，和开始日期 锁定当日数据
⑤根据买入规则，模拟买入 （如果没符合买入规则，跳出循环）
⑥根据卖出规则，模拟卖出（如果最后一个交易日没卖出，强制卖出）
'''



'''
①读detail表，获取日期list
'''
def read_detail():
    df = pd.read_csv(con.detailPath + '2017-10-12-23-21rule+1+10+13detail.csv')
    df = df.sort(columns='date')
    #声明日期list
    dateList = []
    #当前的日期
    dateNow = 0
    dfDate = df['date']
    #循环所有数据，获取日期列表集合
    for date in dfDate:
        #如果日期不同则加入日期列表
        if(dateNow != date):
            dateList.append(date)
        dateNow = date
    return dateList

'''
②根据选定的股票，读取内存中的base csv数据
'''

read_detail()

