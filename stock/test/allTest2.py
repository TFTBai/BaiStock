import pandas as pd
from calculate import calculate as cal
from common import constant as con


def buchang(x):
    return round((1 - (100 / (100 + x))) * 100, 2)


def testMoveCol():
    stock_data = pd.read_csv(con.csvPath + '603999.csv')
    stock_data = stock_data[stock_data['60days'].isnull()]
    # # 输出到csv
    # stock_dataa = stock_data[stock_data['day1closeIncome'] < 0]
    # stock_datab = stock_data[stock_data['day1closeIncome'] >= 0]
    # stock_dataa['day1closeIncome'] = buchang(stock_dataa['day1closeIncome'])
    # stock_data = stock_dataa.append(stock_datab)
    # stock_data.to_csv(con.csvPath + '603999new.csv', index=False)
    print(stock_data)


def testDate():
    stock_data = pd.read_csv(con.csvPath + '603999.csv')
    stock_data = stock_data[stock_data['date'] == '2017-03-23']
    print(stock_data)
