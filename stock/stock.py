'''
负责串联各个模块的总执行
'''
from base import baseStock as bs
from rule import rule
from common import dateUtil

'''
初始化股票基础数据
'''


def init_csv():
    startDate = dateUtil.print_date()
    # bs.create_base()
    bs.create_all_stock_csv()
    bs.create_all_index_csv()
    bs.add_index_derivative_data()
    bs.add_stock_derivative_data()
    # bs.update_all_stock()
    dateUtil.print_end_date(startDate)
    return


'''
更新股票基础数据
'''


def update_csv():
    startDate = dateUtil.print_date()
    bs.add_index_derivative_data()
    bs.add_stock_derivative_data()
    # bs.update_all_stock()
    dateUtil.print_end_date(startDate)
    return



'''
启动股票生成器
'''


def start_stock_generator():
    startDate = dateUtil.print_date()
    # 定义参数类
    class stockArg:
        # total报表命名
        totalCsvName = ''
        # 组合规则
        ruleNumListChoose = []
        # 必须规则
        ruleNumListMust = []
        # 是否按划定日期范围
        dateRangeTF = False
        # 日期范围时间
        dateRange = ''
        # 是否生成detail表
        detail = False

    ''' 基础参数 '''
    stockArg1 = stockArg()
    # total表名称
    stockArg1.totalCsvName = '今日筛选'
    # 是否生成明细表开关
    stockArg1.detail = True
    # 是否生成平均表开关
    stockArg1.mean = False
    # 是否生成保本表开关
    stockArg1.save = False
    # 是否分年开关
    stockArg1.groupByDaysTF = False

    # 是否使用开始日期参数开关
    stockArg1.dateBeginTF = False
    # 开始日期参数
    stockArg1.dateBeginRange = '2017-10-18'
    # 是否使用结束日期参数开关
    stockArg1.dateEndTF = False
    # 结束日期参数
    stockArg1.dateEndRange = '2017-08-10'

    ''' 规则参数 '''
    #成熟规则获取开关,开启时下面定义规则无效
    stockArg1.mustByCsvTF = False
    # stockArg1.ruleNumListChoose = [11,13,21,19]
    # stockArg1.ruleNumListMust = [1,10]
    # 组合规则参数
    stockArg1.ruleNumListChoose = [11]
    # 必选规则参数
    stockArg1.ruleNumListMust = [1,10,19,20]
    # 大盘规则开关
    stockArg1.indexOpen = False

    ''' 策略参数 '''
    # 策略开关
    stockArg1.strategy = False
    # 卖出收益参数(百分点)
    stockArg1.sellIncome = 10

    # 策略买入开关
    stockArg1.buyLineTF = False
    # 策略买入等待天数
    stockArg1.buyLineWaitDays = 3
    # 策略买入线为day0close的加n个百分点
    stockArg1.buyLine = -2
    # 策略买入先期望修正
    stockArg1.buyLineExpect = 0

    # 策略止损线开关
    stockArg1.stopLineTF = False
    # 策略止损线(百分点)
    stockArg1.stopLine = -10
    # 策略止损线期望修正(百分点)
    stockArg1.stopLineExpect = 0

    # 策略失败割肉交易日参数(day几 收盘割肉卖)
    stockArg1.cutMeatDay = 15

    # 执行规则数据生成器方法！
    rule.make_stockData(stockArg1)
    dateUtil.print_end_date(startDate)

# init_csv()
# update_csv()
start_stock_generator()
