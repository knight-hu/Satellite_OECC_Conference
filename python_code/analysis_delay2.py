# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年10月04日
读取延时与路径（测试不同bound结果,最后只用3）
"""

import networkx as nx
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#读取星座参数函数
def read_parameter(path):
    f = open(path)
    line = f.readline()
    line = line.rstrip('\n')
    values = line.split(' ')
    num = len(values)
    parameter = [[0 for i in range(num)] for i in range(6)]
    row = 0
    while line:
        line = line.rstrip('\n')
        values = line.split(' ')
        for i in range(num):
            if row != 0:
                parameter[row][i] = (float)(values[i])
            else:
                parameter[row][i] = values[i]
        row += 1
        line = f.readline()
    f.close()
    return parameter

# 分析周期内延时性能函数
def read_delayinfo():
    global dtime,dpath
    # 读取星座表格数据
    parameter = read_parameter('constellation_parameter.txt')
    constellation_num = len(parameter[0])
    # 分析每一个星座
    for i in range(constellation_num):
        # 读取星座参数
        constellation_name = parameter[0][i]
        satellite_num = int(parameter[1][i])
        constellation_period = int(parameter[2][i])
        bound = int(parameter[5][i])
        city_num =2
        # 设置存储变量
        dtime = [[0 for i in range(constellation_period)] for i in range(1)]
        dpath = [[0 or i in range(1)] for i in range(constellation_period)]
        # 分析星间星地延时
        for time in range(1,constellation_period+1):
        # for time in range(1, 2):
            print(time)
            # 设置环境变量
            edge = []
            # 设置网格变量
            G = nx.Graph()
            # 读取延时变量
            matpath = 'P:\\PRJ-WEIXINGWANG-704\\trunk\\01. 成员工作区\\胡智伟\\05OFC_paper\\Constellation_simulator\\matlab_code\\MegaConstellation\\delay\\' + str(time) + '.mat'
            mat = scio.loadmat(matpath)
            delay = mat['delay']
            # 分析延时
            for i in range(satellite_num):
                # 分析星间延时
                for j in range(i+1,satellite_num):
                    if delay[i][j] > 0:
                        edge.append((i,j,delay[i][j]))
                # 分析星地延时
                for j in range(satellite_num,satellite_num + city_num):
                    if delay[i][j] < bound:
                        edge.append((i,j,delay[i][j]))
            # 添加网格图节点
            G.add_nodes_from(range(satellite_num + city_num))
            # 添加网格点权值
            G.add_weighted_edges_from(edge)
            # 分析北京节点与纽约节点
            count = 0
            for i in range(satellite_num,satellite_num + city_num-1):
                for j in range(i+1,satellite_num + city_num):
                    if nx.has_path(G,source=i,target=j):
                        dtime[count][time-1] = nx.dijkstra_path_length(G,source=i,target=j)
                        dpath[time-1][count] = nx.dijkstra_path(G,source=i,target=j)
                    count += 1


if __name__ == "__main__":
    read_delayinfo()
    np.savetxt('dtime_3.csv', dtime, fmt='%f')
    pd.DataFrame(dpath).to_csv('dpath_3.csv')

# 测试代码
# 保存延时信息
# np.savetxt('edge.csv',edge,fmt = '%f')
# 绘制基础网格图
# nx.draw_networkx(G)
# plt.show()


