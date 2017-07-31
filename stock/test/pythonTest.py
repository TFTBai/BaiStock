import datetime
import itertools

# 获取今天前多少天的日期
def get_the_day_before_today(day):
    today = datetime.date.today()
    tempDate = datetime.timedelta(days=day)
    targetDate = today - tempDate
    return targetDate


# 测试模块间调用
def sayHello():
    print(123)


def isChooseRule(ruleNum, list):
    ruleNum[0] = ruleNum[0] + 1
    if (ruleNum[0] in list):
        return True
    else:
        return False


def testList():
    list = [1, 2,3,4]
    ruleNum = [0]
    if (isChooseRule(ruleNum, list)):
        print('1 is in ')

    if (isChooseRule(ruleNum, list)):
        print('2 is in ')

    if (isChooseRule(ruleNum, list)):
        print('3 is in ')

    if (isChooseRule(ruleNum, list)):
        print('4 is in ')

    if (isChooseRule(ruleNum, list)):
        print('4 is in ')

#计算收益
def jisuanshouyi():
    list = [-0.241,13.16,9.39,3.09,6.39,-0.331,-2.375]
    income = 1
    for a in list:
        income = income*(100+a)/100
    print(income)


'''获取当前日期'''


def get_date_date():
    startDate = datetime.datetime.now().minute
    print(str(startDate))


def test_c_num():
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


