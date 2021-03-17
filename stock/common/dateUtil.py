import datetime

'''
时间相关的工具方法
'''

# 获取今天前多少天的日期
def get_the_day_before_today(day):
    today = datetime.date.today()
    tempDate = datetime.timedelta(days=day)
    targetDate = today - tempDate
    return targetDate


'''获取当前时间'''


def get_date_now():
    startDate = datetime.datetime.now()
    return startDate


'''获取当前日期'''


def get_date_date():
    startDate = datetime.datetime.now().date()
    return startDate
'''获取当前小时'''


def get_hour_and_minute_str():
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    return '-'+str(hour)+'-'+str(minute)




'''获取时间差'''


def get_date_diff(startDate, endDate):
    date_diff = endDate - startDate
    return date_diff


'''打印当前时间'''


def print_date():
    startDate = get_date_now()
    print('当前时间为:' + str(startDate))
    return startDate


'''打印结束时间'''


def print_end_date(startDate):
    endDate = get_date_now()
    print('结束时间为:' + str(endDate) + ',总耗时:' + str(get_date_diff(startDate, endDate)))

