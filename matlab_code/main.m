%% 界面清除
clear all;
clc;

%% 参数设置
global tStart tStop dt name plane_nums sats_plane No_leo;
global No_fac latitude longitude;
dt = 1;
tStart = 0.0;

%% 创建场景
conid = Create_scenario;

%% 新建星座
parameter = Create_satellite;

%% 新建地面站
Create_facility(conid);

%% 存储位置
[position,position_xyz] = Create_position;

%% 计算延时
for t = 1:tStop
    delay = Create_delay(position_xyz,parameter,t);
end

%% 关闭连接
stkClose(conid);
stkClose;