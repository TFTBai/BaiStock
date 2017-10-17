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
获取成熟规则list ps:由于代码结构调整暂不可用,有需求时修改恢复
'''
# def get_one_stock():
#     topList = rule.get_total_list()
#     for mustList in topList:
#         code = rule.make_stockData_by_choose(mustList)
#         if code == 1:
#             print("已找到符合条件的stock 程序运行完毕! ")
#             break
#         else:
#             print("未找到符合条件的stock 程序继续运行!")

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
    stockArg1.detail = False
    # 是否生成平均表开关
    stockArg1.mean = False
    # 是否生成保本表开关
    stockArg1.save = False
    # 是否分年开关
    stockArg1.groupByDaysTF = False

    # 是否使用开始日期参数开关
    stockArg1.dateBeginTF = False
    # 开始日期参数
    stockArg1.dateBeginRange = '2017-01-01'
    # 是否使用结束日期参数开关
    stockArg1.dateEndTF = False
    # 结束日期参数
    stockArg1.dateEndRange = '2017-08-10'

    ''' 规则参数 '''
    stockArg1.ruleNumListChoose = [11,13,19,21,10001]
    stockArg1.ruleNumListMust = [1,10,20]
    # 组合规则参数
    # stockArg1.ruleNumListChoose = [11,13]
    # 必选规则参数
    # stockArg1.ruleNumListMust = [1,10]
    # 大盘规则开关
    stockArg1.indexOpen = True

    ''' 策略参数 '''
    # 策略开关
    stockArg1.strategy = False
    # 卖出收益参数(买入价格的多少倍)
    stockArg1.sellIncome = 1.15
    # 策略失败割肉交易日参数(day几 收盘割肉卖)
    stockArg1.cutMeatDay = 15

    # 执行规则数据生成器方法！
    rule.make_stockData_by_choose(stockArg1)
    dateUtil.print_end_date(startDate)


# init_csv()
# update_csv()
start_stock_generator()
