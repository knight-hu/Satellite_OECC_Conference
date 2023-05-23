# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年09月14日
分析不同阈值bound下节点间延时情况
"""

import numpy as np
import matplotlib.pyplot as plt

# 读取延时信息
def read_path(path):
    f = open(path)
    lines = f.readline()
    lines = lines.rstrip("\n")
    delays = lines.split(" ")
    delays = [float(i) for i in delays]
    return delays

# 绘制延时信息结果
if __name__=='__main__':
    # 读取延时数据
    path_3 = 'dtime_3.csv'
    delays_3 = read_path(path_3)
    length = len(delays_3)
    # 计算平均值与方差
    # mean_delays = np.mean(delays)
    # std_delays = np.std(delays)
    # 时间坐标
    dtime = np.linspace(1,length,length)
    # 绘制每一时刻对应的延时图
    plt.plot(dtime,delays_3,'g-.', label='delay performance')
    # plt.legend(loc="upper center",ncol=2, shadow=True, fancybox=True)
    plt.xlabel('period(s)')
    plt.ylabel('delay(ms)')
    plt.ylim(47.5,51)
    plt.show()