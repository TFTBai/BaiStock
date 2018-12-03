import pandas as pd
from common import dateUtil
from common import constant as con
'''时间成本csv生成方法'''
def getTimeCostCsv():
    print('生成时间成本表开始!')
    #1.获取收益csv
    df = pd.read_csv(con.incomePath + 'gongshiv2.csv', encoding='gbk')
    #2.附加排名列
    df['rank']= range(1,len(df)+1)
    #3.附加时间成本15列
    tcdCols = []
    for n in range(2,16):
        n = str(n)
        timeCostName = 'tcd'+n
        dayCloseMeanName = 'd'+n+'cMean'
        df[timeCostName] = df[dayCloseMeanName]-0.03
        tcdCols.append(timeCostName)
    #4.附加收益最高日列及收益最高日收益列
    df['tdcMaxValue'] = df[tcdCols].max(axis=1)
    df['tdcMaxDay'] = df[tcdCols].idxmax(axis=1).str.replace('tcd','')
    df.to_csv(con.incomePath + str(
        dateUtil.get_date_date()) + dateUtil.get_hour_and_minute_str() + '时间成本收益验证原表' + '.csv',
                               index=False)
    df['dcName'] = 'd'+df['tdcMaxDay']+'cMean'
    df['dcValue'] = df.dcname
