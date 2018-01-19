import pandas as pd
import numpy as np

# df = pd.DataFrame(np.arange(16).reshape(4,4),index=[1,2,3,4],columns=['a','b','c','d'])
df = pd.read_csv('D:\workspace\BaiStock\data\\rulesCsv\gongshiv2.csv')
for index in df.index:
    print(str(df.loc[index]))
    # df1 = df.loc[index][5:20].sort_values(ascending=False)[0:1].index[0]
    # print(df1)
    # df2 = int(df.loc[index][20:34].sort_values(ascending=False)[0:1].index[0].replace('d','').replace('cZ',''))
    # print(df2)
    break
