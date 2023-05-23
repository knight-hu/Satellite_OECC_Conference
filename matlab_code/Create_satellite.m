function parameter = Create_satellite
    % 参数设置
    global name plane_nums sats_plane No_leo tStart dt tStop;
    % 读取星座参数
    path = 'Constellation_parameter.xlsx';
    parameter = readtable(path);
    parameter = parameter.Value;
    name = parameter{1,1};
    altitude = str2num(parameter{2,1});
    period = str2num(parameter{3,1});
    inclination = str2num(parameter{4,1});
    factor = str2num(parameter{5,1});
    plane_nums = str2num(parameter{6,1});
    sats_plane = str2num(parameter{7,1});
    No_leo = plane_nums * sats_plane;
    tStop = period;
    % 轨道6要素
    a = 6371000 + altitude * 1000;
    e = 0;
    inc = inclination * pi / 180;
    w = 0.0;
    if (inclination >80)&&(inclination <100)%极轨道
        raan = [0:180/plane_nums:180-180/plane_nums];
    else%倾斜轨道
        raan = [0:360/plane_nums:360-360/plane_nums];
    end
    raan = raan .* pi / 180;
    mean = [0:360/sats_plane:360-360/sats_plane];
    % 导入轨道
    for i = 1:plane_nums
        for j = 1:sats_plane
            ra = raan(i);
            ma = (mod(mean(j) + 360*factor/(plane_nums*sats_plane)*(i-1),360))*(pi/180);
            num = j + (i-1) * sats_plane;
            if num<10
                sat_no = strcat('Sat000',num2str(num));
            elseif num <100
                sat_no = strcat('Sat00',num2str(num));
            elseif num < 1000
                sat_no = strcat('Sat0',num2str(num));
            else 
                sat_no = strcat('Sat',num2str(num));
            end
            stkNewObj('*/','Satellite',sat_no);
            sat_no = strcat('*/Satellite/',sat_no);
            stkSetPropClassical(sat_no,'J4Perturbation','J2000',tStart,tStop,dt,0,a,e,inc,w,ra,ma);
            num_leo(num) = num;
        end
    end
    save('Num_leo.mat','num_leo');
    mkdir(strcat(name,'\\delay'));
end