# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年09月29日
读取延时与路径第二版(略)
"""
# 导入功能模块
import scipy.io as scio
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 读取星座参数函数
def read_parameter(path):
    # 读取星座个数
    f = open(path)
    line = f.readline()
    line = line.rstrip('\n')
    values = line.split(' ')
    length = len(values)
    # 设置环境变量
    parameter = [[0 for i in range(length)] for i in range(6)]
    row = 0
    # 读取星座数据
    while line:
        line = line.rstrip('\n')
        values = line.split(' ')
        for i in range(length):
            if row != 0:
                parameter[row][i] = float(values[i])
            else:
                parameter[row][i] = values[i]
        row += 1
        line = f.readline()
    f.close()
    return parameter

# 分析延时性能函数
def read_performance():
    # 设置环境变量
    path = 'constellation_parameter.txt'
    parameter = read_parameter(path)
    constellation_num = len(parameter[0])
    # 遍历所有星座数目
    for i in range(constellation_num):
        # 读取星座参数
        constellation_name = parameter[0][i]
        satellite_num = int(parameter[1][i])
        period = int(parameter[2][i])
        bound = int(parameter[5][i])
        # 设置存储变量
        groundcity_num = 2
        dtime = [[0 for i in range(period)] for i in range(constellation_num)]
        dpath = [[0 for i in range(1)] for i in range(period)]
        # 读取延时数据
        for time in range(1,51):
            print(time)
            # 设置环境变量
            edge = []
            # 设置网格变量
            G = nx.Graph()
            # 读取延时变量
            datapath = 'P:\\PRJ-WEIXINGWANG-704\\trunk\\01. 成员工作区\\胡智伟\\05OFC_paper\\Constellation_simulator\\matlab_code\\MegaConstellation\\delay\\' + str(time) + '.mat'
            data = scio.loadmat(datapath)
            delay = data['delay']
            # 分析延时性能
            for i in range(satellite_num):
                # 分析星间延时信息
                for j in range(i+1,satellite_num):
                    if delay[i][j] > 0:
                        edge.append((i,j,delay[i][j]))
                # 分析星地延时信息
                for j in range(satellite_num,satellite_num + groundcity_num):
                    if delay[i][j] < bound:
                        edge.append((i,j,delay[i][j]))
                # 设置网格图节点
                G.add_nodes_from(range(satellite_num + groundcity_num))
                # 设置网格图权值
                G.add_weighted_edges_from(edge)
                # 计算节点间最短路径
                count = 0
                for i in range(satellite_num,satellite_num + 1):
                    for j in range(i+1,satellite_num + groundcity_num):
                        if nx.has_path(G,source=i,target=j):
                            dtime[count][time-1] = nx.dijkstra_path_length(G,source=i,target=j)
                            dpath[time-1][count] = nx.dijkstra_path(G,source=i,target=j)


# 结果分析处理
# 存储延时信息
# np.savetxt('delayinfo.csv',edge,fmt='%f')
# nx.draw_networkx(G)
# plt.show()
# np.savetxt('dtime.csv',dtime,fmt='%f')
# pd.DataFrame(dpath).to_csv('dpath.csv')