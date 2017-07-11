import datetime


# 获取今天前多少天的日期
def get_the_day_before_today(day):
    today = datetime.date.today()
    tempDate = datetime.timedelta(days=day)
    targetDate = today - tempDate
    return targetDate