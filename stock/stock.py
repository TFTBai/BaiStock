'''
负责串联各个模块的总执行
'''
from base import baseStock as bs
from rule import rule

def init_csv():
    bs.create_base()
    bs.create_all_stock_csv()
    bs.add_kmr_data()
    bs.update_all_stock()
    return

def update_csv():
    bs.add_kmr_data()
    bs.update_all_stock()
    return

def get_one_stock():
    topList = rule.get_total_list()
    for mustList in topList:
        code = rule.all_rule(mustList)
        if code == 1:
            print("已找到符合条件的stock 程序运行完毕! ")
            break
        else:
            print("未找到符合条件的stock 程序继续运行!")

update_csv()