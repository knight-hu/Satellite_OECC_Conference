# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年09月30日
"""

import scipy.io as scio
import numpy as np


# 环境变量设置
period = 10
satellite_num = 1000
edge = []
# 读取position变量信息
path= 'P:\\PRJ-WEIXINGWANG-704\\trunk\\01. 成员工作区\\胡智伟\\05OFC_paper\\Constellation_simulator\\matlab_code\\MegaConstellation\\position.mat'
data = scio.loadmat(path)
position = data['position_xyz']
# 存储位置信息
for time in range(1, period + 1):
    for i in range(satellite_num):
        x = position[i][0][0][time-1]*0.001
        y = position[i][0][1][time-1]*0.001
        z = position[i][0][2][time-1]*0.001
        edge.append((time,x,y,z))
np.savetxt('position.txt',edge,fmt = '%f')

