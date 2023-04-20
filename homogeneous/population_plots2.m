function [] = population_plots2(n,t,tspan)
    figure(4)
    tmin = tspan(1);
    tmax = tspan(2);
    t_len = length(t);
    t_step = (tmax-tmin)/t_len;
    t_list = tmin:t_step:tmax-t_step;
    tlen = length(t_list);
    x = 1:100;
    y = zeros(100,3);
    for j = 1
        check = n(j,101:200);
        y(:,1) = n(j,101:200);
        snapshot = plot(x,y);
        gifwrite(snapshot,{1},'metastaticinvasion.gif');
    end
    y = zeros(100,3);
    for j = 2:tlen
        check = n(j,101:200);
        y(1,:) = n(j,101:200);
        snapshot = plot(x,y);
        gifwrite(snapshot,'metastaticinvasion.gif');
    end
end