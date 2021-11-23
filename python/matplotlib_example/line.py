import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = np.random.randn(5,3)
df = pd.DataFrame(np.abs(data),
                  index=['Mon', 'Tue', 'Wen', 'Thir', 'Fri'],
                  columns=['A', 'B', 'C'])

df

# 折线图
# 两行, 是不是简单到爆
# 关于plot更多参数查看: help(df.plot)
df.plot()
plt.show()

# 柱状图
df.A.plot(kind='bar', title='I am Mon')
plt.show()

# 多重柱状图
df.plot(kind='bar', title='From Mon To Fri')
plt.show()
