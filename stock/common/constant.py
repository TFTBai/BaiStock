csvPath = 'D:/workSpace/BaiStock/data/csv/'
indexCsvPath = 'D:/workSpace/BaiStock/data/indexCsv/'
basePath = 'D:/workSpace/BaiStock/data/'
detailPath = 'D:/workSpace/BaiStock/data/detail/'
incomeDay = 31
# 几日列表
high_percent_list = [1.8, 1.9, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7]
baseIndexList = ['000001', '399001', '399006']
shenIndex = '399001'
chuangIndex = '399006'
shangIndex = '000001'
shenIndexBegin = '00'
chuangIndexBegin = '30'
shangIndexBegin = '60'
shangBIndexBegin = '90'


allBaseNameOrderBak = ['code', 'open', 'close', 'high', 'low', 'price_change', 'p_change', 'volume', 'volume5days',
                    'volume10days', 'volume30days',
                    'day1o/day0c', 'day1highIncome', 'day1closeIncome', 'day2highIncome', 'day2closeIncome',
                    'day3highIncome', 'day3closeIncome',
                    'day4highIncome', 'day4closeIncome', 'day5highIncome', 'day5closeIncome', 'day6highIncome',
                    'day6closeIncome', '2days', '5days', '30days', '60days', 'kdj_k', 'kdj_d',
                    'kdj_j', 'macd', 'macd_DIFF', 'macd_DEA', 'rsi6', 'rsi12', 'rsi24']

'''
添加几日收益数据
'''
def get_day_list(day):
    day_list = []
    day_list_index = 0
    while day_list_index < day:
        day_list_index = day_list_index+1
        day_list.append(day_list_index)
    return day_list

day_list = get_day_list(6)

'''
添加默认排序
'''
def getAllBaseNameOrder(day):
    nameList = ['code', 'open', 'close', 'high', 'low', 'price_change', 'p_change', 'volume', 'volume5days',
     'volume10days', 'volume30days','day1o/day0c', '2days', '5days', '30days', '60days', 'kdj_k', 'kdj_d',
     'kdj_j', 'macd', 'macd_DIFF', 'macd_DEA', 'rsi6', 'rsi12', 'rsi24']
    nameListIndex = 0
    nameListStringClose = 'closeIncome'
    nameListStringHigh = 'highIncome'
    nameListStringOpen = 'openIncome'
    while nameListIndex < day:
        nameListIndex = nameListIndex + 1
        nameList.append('day'+str(nameListIndex)+nameListStringClose)
    nameListIndex = 0
    while nameListIndex < day:
        nameListIndex = nameListIndex + 1
        nameList.append('day' + str(nameListIndex) + nameListStringHigh)
    nameListIndex = 0
    while nameListIndex < day:
        nameListIndex = nameListIndex + 1
        nameList.append('day' + str(nameListIndex) + nameListStringOpen)
    return nameList

allBaseNameOrder = getAllBaseNameOrder(6)



