function [position,position_xyz] = Create_position
    % 设置变量
    global No_leo No_fac tStart tStop dt latitude longitude name;
    % 下载数据
    load('Num_leo.mat');
    load('Num_fac.mat');
    % 设置存储空间
    position = cell(No_leo + No_fac,1);
    position_xyz = cell(No_leo + No_fac,1);
    index = 1;
    % 存储卫星位置
    for i = 1:No_leo
        if i<10
            sat_info = strcat('*/Satellite/Sat000',num2str(i));
        elseif i<100
            sat_info = strcat('*/Satellite/Sat00',num2str(i));
        elseif i<1000
            sat_info = strcat('*/Satellite/Sat0',num2str(i));
        else
            sat_info = strcat('*/Satellite/Sat',num2str(i));
        end
        [secData,secNames] = stkReport(sat_info,'LLA Position',tStart,tStop,dt);
        lat = stkFindData(secData{1},'Lat');
        long = stkFindData(secData{1},'Lon');
        alt = stkFindData(secData{1},'Alt');
        llapos = zeros(3,tStop);
        for j = 1:tStop
            llapos(1,j) = llapos(1,j) + lat(j)*180/pi;
            llapos(2,j) = llapos(2,j) + long(j)*180/pi;
            llapos(3,j) = llapos(3,j) + alt(j);
        end
        position{index} = llapos;
        position_xyz{index} = Convert_xyz(position{index,1});
        index = index + 1;
    end
    % 存储地面站位置
    for i = 1:No_fac
        llapos = zeros(3,tStop);
        llapos(1,:) = llapos(1,:) + latitude(i);
        llapos(2,:) = llapos(2,:) + longitude(i);
        position{index} = llapos;
        position_xyz{index} = Convert_xyz(position{index,1});
        index = index + 1;
    end
    % 存储位置信息
    filename = [name '\position.mat'];
    save(filename,'position','position_xyz');
end