import pandas as pd
import matplotlib.pyplot as plt

plt.rc("font", family='Songti SC')  # 解决中文不显示问题

df = pd.read_excel('/Users/chenpuyu/Documents/个人/宝宝/宝宝记录.xlsx',
                   sheet_name=1, index_col='日期')

dairy_df = df[['总奶量', '母乳量', '配方奶']]

dairy_df.plot()
plt.show()

# 柱状图
dairy_df['总奶量'].plot(kind='bar', title='总奶量')
plt.show()

# 多列柱形图
dairy_df.plot(kind='bar', title='多列柱形图')
plt.show()

# # 堆积图
dairy_df[['母乳量', '配方奶']].plot(kind='bar', stacked=True)
plt.show()
