# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年10月04日
读取拓扑结构中介中心度
"""

import networkx as nx
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import sample

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

# 对网格图进行分析函数
def read_networkx():
    global dtime,dpath,G
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
        city_num = 2
        # 设置存储变量
        dtime = [[0 for i in range(constellation_period)] for i in range(1)]
        dpath = [[0 or i in range(1)] for i in range(constellation_period)]
        # 分析星间星地延时
        for time in range(1, 1 + 1):
            # print(time)
            # 设置环境变量
            edge = []
            # 设置网格变量
            G = nx.Graph()
            # 读取延时变量
            matpath = 'P:\\PRJ-WEIXINGWANG-704\\trunk\\01. 成员工作区\\胡智伟\\05OFC_paper\\Constellation_simulator\\matlab_code\\MegaConstellation\\delay\\' + str(
                time) + '.mat'
            mat = scio.loadmat(matpath)
            delay = mat['delay']
            # 分析延时
            for i in range(satellite_num):
                # 分析星间延时
                for j in range(i + 1, satellite_num):
                    if delay[i][j] > 0:
                        edge.append((i, j, delay[i][j]))
                # 分析星地延时
                for j in range(satellite_num, satellite_num + city_num):
                    if delay[i][j] < bound:
                        edge.append((i, j, delay[i][j]))
            # 添加网格图节点
            G.add_nodes_from(range(satellite_num + city_num))
            # 添加网格点权值
            G.add_weighted_edges_from(edge)


if __name__ == '__main__':
    read_networkx()
    try:
        # compute centrality
        centrality = nx.betweenness_centrality(G, k=10, endpoints=True)
        print(centrality)

        # compute community structure
        lpc = nx.community.label_propagation_communities(G)
        community_index = {n: i for i, com in enumerate(lpc) for n in com}

        #### draw graph ####
        fig, ax = plt.subplots(figsize=(20, 15))
        pos = nx.spring_layout(G, k=0.15, seed=4572321)
        node_color = [community_index[n] for n in G]
        node_size = [v * 20000 for v in centrality.values()]
        nx.draw_networkx(G,pos=pos,with_labels=False,node_color=node_color,node_size=node_size,edge_color="gainsboro",alpha=0.4,)

        # Title/legend
        font = {"color": "k", "fontweight": "bold", "fontsize": 20}
        ax.set_title("Gene functional association network (C. elegans)", font)
        # Change font color for legend
        font["color"] = "r"

        ax.text(
            0.80,
            0.10,
            "node color = community structure",
            horizontalalignment="center",
            transform=ax.transAxes,
            fontdict=font,
        )
        ax.text(
            0.80,
            0.06,
            "node size = betweeness centrality",
            horizontalalignment="center",
            transform=ax.transAxes,
            fontdict=font,
        )

        # Resize figure for label readibility
        ax.margins(0.1, 0.05)
        fig.tight_layout()
        plt.axis("off")
        plt.show()
    except nx.NetworkXNoPath:
        print('No Path!')

    # 构建网格图中最短路径分布的直方图
    # 查找路径长度
    # length_source_target = dict(nx.shortest_path_length(G))
    # print(length_source_target)
    '''
    # 将字典转换为列表
    all_shortest = sum([list(length_target.values())
    for length_target in length_source_target.values()],[])
    # 计算整数bins
    high = max(all_shortest)
    bins = [-0.5 + i for i in range(high + 2)]
    print(bins)
    # 绘制直方图
    plt.hist(all_shortest, bins=bins, rwidth=0.8)
    plt.xlabel("Distance")
    plt.ylabel("Count")
    plt.show()
    '''

    # nx.draw_networkx(G)
    # plt.show()