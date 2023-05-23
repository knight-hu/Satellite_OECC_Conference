# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年09月14日
读取延时与路径
"""

import networkx as nx
import scipy.io as scio
import numpy as np

# 读取星座参数
def read_parameter(path):
    f = open(path)
    line = f.readline()
    line = line.rstrip('\n')
    values = line.split(' ')
    # 设置环境变量
    parameter = [[0 for i in range(len(values))] for i in range(6)]
    row = 0
    # 变量数据写入
    while line:
        line = line.rstrip('\n')
        values = line.split(' ')
        for i in range(len(values)):
            if row != 0:
                parameter[row][i] = (float)(values[i])
            else:
                parameter[row][i] = values[i]
        row += 1
        line = f.readline()
    f.close()
    return parameter

# 读取网络延时性能
def read_performance():
    # 读取星座参数
    path = 'constellation_parameter.txt'
    parameter = read_parameter(path)
    # 分析延时性能
    constellation_num = len(parameter[0])
    for i in range(constellation_num):
        constellation_name = parameter[0][i]
        satellite_num = int(parameter[1][i])
        period = int(parameter[2][i])
        bound = int(parameter[5][i])
        city_num = 2
        dt = 1
        # 设置环境变量
        # 分析端到端 北京-纽约 周期内
        dtime = [[0 for i in range(int((period-1)//dt) + 1)] for i in range(1)]
        # 出现错误情况
        error = [0 for i in range(1)]
        for time in range(1,period + 1,dt):
            print(time)
            # 设置网格环境
            G = nx.Graph()
            edge = []
            # 读取延时变量
            path = 'P:\\PRJ-WEIXINGWANG-704\\trunk\\01. 成员工作区\\胡智伟\\05OFC_paper\\Constellation_simulator\\matlab_code\\' + constellation_name + '\\delay\\' + str(time) + '.mat'
            data = scio.loadmat(path)
            delay  = data['delay']
            # 网格图添加卫星节点
            G.add_nodes_from(range(satellite_num+city_num))
            # 添加边权值
            for i in range(satellite_num):
                # 添加星间边权值
                for j in range(i+1,satellite_num):
                    if delay[i][j] > 0:
                        edge.append((i,j,delay[i][j]))
                # 添加星地边权值
                for j in range(satellite_num,satellite_num+city_num):
                    if delay[i][j] < bound:
                        edge.append((i,j,delay[i][j]))
            # 网格图添加边权值
            G.add_weighted_edges_from(edge)

            # 网格图上分析城市间延时性能
            count = 0
            for i in range(satellite_num,satellite_num+city_num-1):
                for j in range(i+1,satellite_num+city_num):
                    if nx.has_path(G,source=i,target=j):
                        # 计算北京到纽约最短延时总和
                        dtime[count][int((time-1)//dt)] = nx.dijkstra_path_length(G,source=i,target=j)
                    else:
                        error[count] += 1
                        dtime[count][(time-1)//dt] = 0
                    count += 1
        # 存储城市间延时结果
        np.savetxt(constellation_name+'.csv',dtime,fmt='%f')

if __name__ == '__main__':
    read_performance()