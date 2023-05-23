function conid = Create_scenario
    % 参数设置
    global dt;
    %建立连接
    remMachine = stkDefaultHost;
    conid = stkOpen(remMachine);
    % 判断当前场景
    scen_open = stkValidScen;
    if scen_open == 1
        rtn = questdlg('Close the current scenario?');
        if ~strcmp(rtn,'Yes')
            stkClose(conid);%关闭连接
        else
            stkUnload('/*');%关闭场景
        end
    end
    % 新建场景
    stkNewObj('/','Scenario','constellation_scenario');
    % 场景时间设置
    stkSetTimePeriod('13 Sep 2022 0:00:00.0','14 Sep 2022 10:00:00.0','GREGUTC');
    stkSetEpoch('13 Sep 2022 0:00:00.0','GREGUTC');
    % 场景动画设置
    cmd1 = ['SetValues "13 Sep 2022 0:00:00.0" ' mat2str(dt)];
    cmd1 = [cmd1 ' 0.1'];
    rtn = stkConnect(conid,'Animate','Scenario/constellation_scenario',cmd1);
    rtn = stkConnect(conid,'Animate','Scenario/constellation_scenario','Reset');
end