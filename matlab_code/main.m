%% �������
clear all;
clc;

%% ��������
global tStart tStop dt name plane_nums sats_plane No_leo;
global No_fac latitude longitude;
dt = 1;
tStart = 0.0;

%% ��������
conid = Create_scenario;

%% �½�����
parameter = Create_satellite;

%% �½�����վ
Create_facility(conid);

%% �洢λ��
[position,position_xyz] = Create_position;

%% ������ʱ
for t = 1:tStop
    delay = Create_delay(position_xyz,parameter,t);
end

%% �ر�����
stkClose(conid);
stkClose;