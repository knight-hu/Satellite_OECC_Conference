# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年10月08日
不同选路下延时与跳数柱形图
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 字体设置
config = {  "font.family": 'Times New Roman',
            "font.size": 12,
            'axes.unicode_minus': False
         }
rcParams.update(config)


# 设置空环境变量
bandwidth = []

# 遇到障碍点删除部分节点 方式1--16/49.52055458146921
# delete_node = [201,924] # 方式2--17/52.328989217461896
# delete_node = [201,924,661,385,641] # 方式3--18/55.15507944652391
# delete_node = [385] # 方式4--19/52.18465692293163
# delete_node = [201,385,283,661,662] # 方式5--20/53.80686909728116
delay = [49.52055458146921,52.328989217461896, 55.15507944652391,52.18465692293163,53.80686909728116]
jump = [16,17,18,19,20]

intercity = ['Dijkstra','Path1','Path2','Path3','Path4']
index = np.arange(len(intercity))


# 绘制柱形图
plt.bar(index,delay,width = 1/3,label = 'delays',color = 'blue')
plt.bar(index+1/3,jump,width = 1/3,label = 'jumps',color = 'red')

'''
plt.bar(index,bandwidth0,width = 1/4,label = 'StarLink')
plt.bar(index+1/4,bandwidth1,width = 1/4,label = 'OneWeb',color = 'red')
plt.bar(index+2/4,bandwidth2,width = 1/4,label = 'polar_Telesat',color = 'yellow')
'''

# 完善图形显示
plt.legend(ncol = 2,loc = 'best')
plt.xticks(index+1/3,intercity)
plt.ylabel('Delays and jumps(ms)')
plt.ylim(0,62)
plt.show()

