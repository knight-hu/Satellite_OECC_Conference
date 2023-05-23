function Create_facility(conid)
    % 参数设置
    global latitude longitude No_fac;
    % 城市位置（BJ&NY）
    latitude = [39.9 40.42];
    longitude = [116.3 -74];
    No_fac = length(latitude);
    for i = 1:No_fac
        fac_no = strcat('Fac',num2str(i));
        stkNewObj('*/','Facility',fac_no);
        lat = latitude(i);
        long = longitude(i);
        fac_no = strcat('Scenario/constellation_scenario/Facility/',fac_no);
        stkSetFacPosLLA(fac_no,[lat*pi/180; long*pi/180; 0]);
        stkConnect(conid,'SetConstraint',fac_no,'ElevationAngle Min 20');
        num_fac(i) = i;
    end
    save('Num_fac.mat','num_fac');
end