import itertools

'''
生成输入数组的所有组合
'''
def get_all_combinations(numlist):
    listAll = []
    for i in range(1, len(numlist) + 1):
        iter = itertools.combinations(numlist, i)
        listAll.append(list(iter))
    return listAll

'''
根据detail，获取日期list
'''
def get_detail_date(detail):
    detail = detail.sort(columns='date')
    #声明日期list
    dateList = []
    #当前的日期
    dateNow = 0
    detailDate = detail['date']
    #循环所有数据，获取日期列表集合
    for date in detailDate:
        #如果日期不同则加入日期列表
        if(dateNow != date):
            dateList.append(date)
        dateNow = date
    return dateList

'''
取list平均值返回
'''
def get_mean_by_list(list):
    # 声明累加总和
    sum = 0
    for data in list:
        sum = sum + data
    mean = round(sum/len(list),3)
    return mean

'''
根据百分点返回倍数
'''
def get_multiple_by_percentage(percentage):
    return 1+(percentage/100)
