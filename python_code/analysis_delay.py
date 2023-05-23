# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年09月14日
最开始读取延时dtime与路径dpath
"""

import networkx as nx
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 读取星座参数函数
def read_parameter(path):
    f = open(path)
    line = f.readline()
    line = line.rstrip('\n')
    values = line.split(' ')
    # 设置环境变量
    parameter = [[0 for i in range(len(values))] for i in range(6)]
    row = 0
    # 参数写进变量
    while line:
        line = line.rstrip('\n')
        values = line.split(' ')
        for i in range(len(values)):
            if row != 0:
                parameter[row][i] = float(values[i])
            else:
                parameter[row][i] = values[i]
        row += 1
        line = f.readline()
    f.close()
    return parameter

# 分析延时网络性能
def read_performance():
    path = 'constellation_parameter.txt'
    parameter = read_parameter(path)
    constellation_num = len(parameter[0])
    # 读取每一个星座
    for i in range(constellation_num):
        # 读取星座参数
        constellation_name = parameter[0][i]
        satellite_num = int(parameter[1][i])
        constellation_period = int(parameter[2][i])
        bound = parameter[5][i]
        # 增加参数设置
        city_num = 2
        # 设置环境变量
        dtime = [[0 for i in range(constellation_period)] for i in range(1)]
        dpath = [[0 for i in range(1)] for i in range(constellation_period)]
        error = [0 for i in range(1)]
        # 读取周期内延时信息5731
        for time in range(1,constellation_period + 1):
            print(time)
            # 设置网格环境
            G = nx.Graph()
            edge = []
            G.add_nodes_from(range(satellite_num + city_num))
            # 读取延时变量
            path = 'P:\\PRJ-WEIXINGWANG-704\\trunk\\01. 成员工作区\\胡智伟\\05OFC_paper\\Constellation_simulator\\matlab_code\\' + constellation_name + '\\delay\\' + str(time) + '.mat'
            data = sio.loadmat(path)
            delay = data['delay']
            # 对延时分析
            for i in range(satellite_num):
                # 分析星间延时
                for j in range(i+1,satellite_num):
                    if delay[i][j] > 0:
                        edge.append((i,j,delay[i][j]))
                # 分析城市间延时
                for j in range(satellite_num,satellite_num+city_num):
                    if delay[i][j] < bound:
                        edge.append((i,j,delay[i][j]))
            # 网格添加边权值
            G.add_weighted_edges_from(edge)
            # 网格图进行两城市间分析
            count = 0
            for i in range(satellite_num,satellite_num+city_num-1):
                for j in range(i+1,satellite_num+city_num):
                    if nx.has_path(G,source=i,target=j):
                        dtime[count][time-1] = nx.dijkstra_path_length(G,source=i,target=j)
                        dpath[time-1][count] = nx.dijkstra_path(G,source=i,target=j)
                    else:
                        error[count] += 1
                        dtime[count][time-1] = 0
                    count += 1
        np.savetxt('path_length.csv',dtime,fmt='%f')
        pd.DataFrame(dpath).to_csv('path.csv')

if __name__ == '__main__':
    read_performance()
    print(dtime)