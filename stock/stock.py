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
    bs.create_base()
    bs.create_all_stock_csv()
    bs.add_kmr_data()
    bs.update_all_stock()
    dateUtil.print_end_date(startDate)
    return


'''
更新股票基础数据
'''


def update_csv():
    startDate = dateUtil.print_date()
    bs.add_kmr_data()
    bs.update_all_stock()
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

    # 参数组合1
    stockArg1 = stockArg()
    stockArg1.totalCsvName = '测试'
    stockArg1.ruleNumListChoose = [10]
    stockArg1.ruleNumListMust = [18]
    stockArg1.detail = True
    stockArg1.mean = True
    stockArg1.dateRangeTF = True
    stockArg1.dateRangeTF = '2017-05-01'

    # 执行规则数据生成器方法
    rule.make_stockData_by_choose(stockArg1)
    dateUtil.print_end_date(startDate)


start_stock_generator()
