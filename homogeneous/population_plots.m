function [] = population_plots(n,t,tspan)

    figure(1)
    plot(t,n(:,1), t, n(:,2))
    xlabel('time') 
    ylabel('Number of clusters') 
    legend('n=1', 'n=2')

    figure(2)
    plot(1:100, n(1,1:100), '-o', 1:100, n(40,1:100),'-o', 1:100, n(end,1:100),'-o')
    xlabel('Size of cluster') 
    ylabel('Number of clusters') 
    legend('t=0','t = mid', 't=end')

    figure(3)
    tmin = tspan(1);
    tmax = tspan(2);
    t_len = length(t);
    t_step = (tmax-tmin)/t_len;
    t_list = tmin:t_step:tmax-t_step;
    tlen = length(t_list);
    x = 1:100;

    for j = 1
        y = n(j,1:100);
        plot(x,y);
        gif('clustersize.gif','overwrite',true);
    end
    for j = 2:tlen
        y = n(j,1:100);
        plot(x,y);
        gif;
    end
    
end