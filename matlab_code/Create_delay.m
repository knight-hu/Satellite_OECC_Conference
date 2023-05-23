function delay = Create_delay(position_xyz,parameter,time)
    % 设置变量
    global No_leo No_fac plane_nums sats_plane name;
    % 下载数据
    load('Num_leo.mat');
    load('Num_fac.mat');
    % 设置环境变量
    distance = zeros(No_leo+No_fac,No_leo+No_fac);
    delay = zeros(No_leo+No_fac,No_leo+No_fac);
    % 计算星间关系
    for i = 1:plane_nums
        for j = 1:sats_plane
            cur_leo = (i-1)*sats_plane + j;
            % 轨道内链路关系
            if j~=sats_plane
                up_leo = (i-1)*sats_plane + j + 1;
            else
                up_leo = (i-1)*sats_plane +1;
            end
            distance(cur_leo,up_leo) = sqrt((position_xyz{cur_leo,1}(1,time)-position_xyz{up_leo,1}(1,time))^2 + (position_xyz{cur_leo,1}(2,time)-position_xyz{up_leo,1}(2,time))^2 + (position_xyz{cur_leo,1}(3,time)-position_xyz{up_leo,1}(3,time))^2);
            distance(up_leo,cur_leo) = distance(cur_leo,up_leo);
            delay(cur_leo,up_leo) = distance(cur_leo,up_leo)/(3*10^5);
            delay(up_leo,cur_leo) = delay(cur_leo,up_leo);
            % 轨道间链路关系
            if i~= plane_nums
                right_leo = i*sats_plane + j;
            else
                if (str2num(parameter{4,1})>80 && str2num(parameter{4,1})<100)
                    continue;
                else
                    right_leo = j;
                end
            end
            distance(cur_leo,right_leo) = sqrt((position_xyz{cur_leo,1}(1,time)-position_xyz{right_leo,1}(1,time))^2 + (position_xyz{cur_leo,1}(2,time)-position_xyz{right_leo,1}(2,time))^2 + (position_xyz{cur_leo,1}(3,time)-position_xyz{right_leo,1}(3,time))^2);
            distance(right_leo,cur_leo) = distance(cur_leo,right_leo);
            delay(cur_leo,right_leo) = distance(cur_leo,right_leo)/(3*10^5);
            delay(right_leo,cur_leo) = delay(cur_leo,right_leo);
        end
    end
    % 计算星地关系
    for i = 1:No_leo
        for j = No_leo+1:No_leo+No_fac
            distance(i,j) = sqrt((position_xyz{i,1}(1,time)-position_xyz{j,1}(1,time))^2 + (position_xyz{i,1}(2,time)-position_xyz{j,1}(2,time))^2 + (position_xyz{i,1}(3,time)-position_xyz{j,1}(3,time))^2);
            distance(j,i) = distance(i,j);
            delay(i,j) = distance(i,j)/(3*10^5);
            delay(j,i) = delay(i,j);
        end
    end
    filename = [name '\delay\'];
    filename = strcat(filename,num2str(time));
    filename = strcat(filename,'.mat');
    save(filename,'delay');
end