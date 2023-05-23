function position_xyz = Convert_xyz(position)
    R = 6371 * 10^3;
    r = R + position(3,:);
    Theta = pi/2 - position(1,:)*pi/180;
    Phi = 2*pi + position(2,:)*pi/180;
    X = (r.*sin(Theta)).*cos(Phi);
    Y = (r.*sin(Theta)).*sin(Phi);
    Z = r.*cos(Theta);
    position_xyz = [X;Y;Z];
end