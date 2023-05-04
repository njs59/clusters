function [] = population_plots(n,t,tspan)
    global N
    figure(1)
    plot(t,n(:,1), t, n(:,2))
    xlabel('time') 
    ylabel('Number of clusters') 
    legend('n=1', 'n=2')

    figure(2)
    plot(1:N, n(1,1:N), '-o', 1:N, n(40,1:N),'-o', 1:N, n(end,1:N),'-o')
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
    x = 1:N;

    for j = 1
        y = n(j,1:N);
        plot(x,y);
        gif('clustersize.gif','overwrite',true);
    end
    for j = 2:tlen
        y = n(j,1:N);
        plot(x,y);
        gif;
    end
    
end