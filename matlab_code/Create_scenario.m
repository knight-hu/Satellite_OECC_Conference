function conid = Create_scenario
    % ��������
    global dt;
    %��������
    remMachine = stkDefaultHost;
    conid = stkOpen(remMachine);
    % �жϵ�ǰ����
    scen_open = stkValidScen;
    if scen_open == 1
        rtn = questdlg('Close the current scenario?');
        if ~strcmp(rtn,'Yes')
            stkClose(conid);%�ر�����
        else
            stkUnload('/*');%�رճ���
        end
    end
    % �½�����
    stkNewObj('/','Scenario','constellation_scenario');
    % ����ʱ������
    stkSetTimePeriod('13 Sep 2022 0:00:00.0','14 Sep 2022 10:00:00.0','GREGUTC');
    stkSetEpoch('13 Sep 2022 0:00:00.0','GREGUTC');
    % ������������
    cmd1 = ['SetValues "13 Sep 2022 0:00:00.0" ' mat2str(dt)];
    cmd1 = [cmd1 ' 0.1'];
    rtn = stkConnect(conid,'Animate','Scenario/constellation_scenario',cmd1);
    rtn = stkConnect(conid,'Animate','Scenario/constellation_scenario','Reset');
end