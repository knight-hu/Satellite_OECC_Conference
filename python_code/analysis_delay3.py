# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年10月08日
通过删除节点的方式得到不同选路
"""

import networkx as nx
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import random


WALKABLE = 'walkable'

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
    global dtime,dpath,dtime1,dpath1,dtime2
    # 读取星座表格数据
    parameter = read_parameter('constellation_parameter.txt')
    constellation_num = len(parameter[0])
    # 分析每一个星座
    for i in range(constellation_num):
        # 读取星座参数
        constellation_name = parameter[0][i]
        satellite_num = int(parameter[1][i])
        constellation_period = int(parameter[2][i])
        bound = int(parameter[3][i])
        city_num =2
        # 设置存储变量
        # 分析任1时刻星间星地延时
        for time in range(1,1+1):
            # 设置环境变量
            edge = []
            # 设置网格变量
            G = nx.Graph()
            # 读取延时变量
            matpath = 'P:\\PRJ-WEIXINGWANG-704\\trunk\\01. 成员工作区\\胡智伟\\05OFC_paper\\Constellation_simulator\\matlab_code\\MegaConstellation\\delay\\' + str(500) + '.mat'
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
            # 遇到障碍点删除部分节点 方式1--16/49.52055458146921
            # delete_node = [201,924] # 方式2--17/52.328989217461896
            # delete_node = [201,924,661,385,641] # 方式3--18/55.15507944652391
            # delete_node = [385] # 方式4--19/52.18465692293163
            # delete_node = [201,385,283,661,662] # 方式5--20/53.80686909728116
            # G.remove_nodes_from(delete_node)

            # 分析北京节点与纽约节点
            # count = 0
            for i in range(satellite_num,satellite_num + city_num-1):
                for j in range(i+1,satellite_num + city_num):
                    if nx.has_path(G,source=i,target=j):
                        # dijkstra路径及对应时长
                        dpath = nx.dijkstra_path(G,source=i,target=j)
                        dtime = nx.dijkstra_path_length(G,source=i,target=j)
                        # 两点间最短路径及对应跳数
                        dpath1 = nx.shortest_path(G,source=i,target=j)
                        dtime1 = nx.shortest_path_length(G,source=i,target=j)
                        # 计算整个图的平均最短路径长度
                        dtime2 = nx.average_shortest_path_length(G)


if __name__ == "__main__":
    read_delayinfo()
    print(dpath,dtime)
    print(dpath1,dtime1)
    print(dtime2)