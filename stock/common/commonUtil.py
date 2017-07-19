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