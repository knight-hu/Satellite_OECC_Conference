# -*- coding:utf-8 -*-
"""
作者：huzhiwei
日期：2022年09月29日
绘制三维拓扑图
"""

import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animmation

# 更新星座卫星
def update(time):
    global line, text
    for i in range(len(position[time])):
        lineTemp = line[i]
        # 更新卫星位置
        lineTemp.set_data(position[time][i][0], position[time][i][1])
        lineTemp.set_3d_properties(position[time][i][2])
        # 更新卫星注释位置
        # textSat = text[i]
        # textSat.remove()
        # textSat = ax.text(position[time][i][0], position[time][i][1], position[time][i][2], "satellite" + str(i))
        # text[i] = textSat

# 初始化星座卫星
def init():
    global line,ax
    line = []
    for i in range(len(position[0])):
        # 卫星的初始位置
        line3, = ax.plot([position[0][i][0]], [position[0][i][1]], [position[0][i][2]], marker='o', color='red',markersize=4)
        line.append(line3)
        # 卫星的注释
        # textSat = ax.text(position[0][i][0], position[0][i][1], position[0][i][2], "s"+str(i))
        # text.append(textSat)

# 读取position.txt文件
def read(readFile):
    global time, position
    f = open(readFile, "r")
    time = []
    position = []
    index = 0
    for each_line in f:
        if (index % 1000 == 0):position.append([])
        index += 1
        t,a, b, c = each_line.split(" ")
        time.append((float)(t))
        temp = []
        temp.append(float(a))
        temp.append(float(b))
        c = c.rstrip("\n")  # 可能c尾部有\n，要去掉
        temp.append(float(c))
        position[-1].append(temp)
    f.close()

# 绘制三维结构图
def draw(num, inclination, r, color, ax, omega1, t_range):
    x0 = r * np.cos(omega1 * t_range)
    y0 = r * np.sin(omega1 * t_range)
    z0 = 0
    # 绘制坐标
    x1 = x0
    y1 = np.cos(inclination) * y0 - np.sin(inclination) * z0
    z1 = np.sin(inclination) * y0 + np.cos(inclination) * z0
    # 星座轨道数目
    dengcha = 360 // num
    for i in range(num):
        shengjiaodian = dengcha * i * np.pi / 180
        x2 = np.cos(shengjiaodian) * x1 - np.sin(shengjiaodian) * y1
        y2 = np.sin(shengjiaodian) * x1 + np.cos(shengjiaodian) * y1
        z2 = z1
        ax.plot(x2, y2, z2, color)

# 绘制地球图形
def earth():
    global ax,f
    R = 6371  # 地球半径
    r = 6371 + 550  # 卫星高度
    inc = 53 * np.pi / 180  # 倾斜角rad
    # 设置显示界面
    f = plt.figure(figsize=(12, 12))
    ax = f.add_subplot(111, projection='3d')
    ax.set_title("MegaConstellation Model")
    # 地球模型
    ax.plot([0], [0], [0], marker='o', color='lightblue', markersize=220)
    # 坐标信息，包括坐标长度和单位
    ax.set_xlim([-(r + 200), (r + 200)])
    ax.set_xlabel('X/km')
    ax.set_ylim([-(r + 200), (r + 200)])
    ax.set_ylabel('Y/km')
    ax.set_zlim([-(r + 200), (r + 200)])
    ax.set_zlabel('Z/km')
    # 设置参数信息
    omega1 = 2 * np.pi
    t_range = np.arange(0, 1 + 0.005, 0.005)
    t_len = len(t_range)
    # 画550km高度的卫星轨道
    draw(50, inc, r, 'purple', ax, omega1, t_range)

# 主函数运行
if __name__ == '__main__':
    # 绘制可视化基本结构
    earth()
    # 读取位置与时间信息
    read('position.txt')
    # print(time)
    # print(position)
    # print(position[1][0][2])
    # 初始化星座结构
    init()
    # update(5)
    # print(len(position[1]))
    # ani = animmation.FuncAnimation(f, update, frames=[i for i in range(len(position))], init_func=init, interval=20)
    # ani.save('planet.gif', writer='imagemagick', fps=40)
    plt.show()
