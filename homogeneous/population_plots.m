function [] = population_plots(n,t,tspan, derivative_l2_norm)
    global N
    %figure(1)
    %plot(t,n(:,1), t,n(:,2), t,n(:,10), t,n(:,40))
    %xlabel('time') 
    %ylabel('Number of clusters')
    %xlim([0 2])
    %ylim([0 60])
    %legend('n=1', 'n=2', 'n=10', 'n=40')

    figure(2)
    
    t_10 = find(t > 10, 1);
    t_50 = find(t > 50, 1);
    disp('t_10 is')
    disp(t_10)
    disp('t_50 is')
    disp(t_50)
    t_1000 = find(t > 1000, 1);
    disp('t_1000 is')
    disp(t_1000)
    t_10000 = find(t > 10000, 1);
    disp('t_10000 is')
    disp(t_10000)
    t_20000 = find(t > 20000, 1);
    disp('t_20000 is')
    disp(t_20000)
    %1:N, n(t_1000,1:N),'-o', 1:N, n(t_10000,1:N),'-o',  1:N, 

    plot(1:N, n(1,1:N), '-o', 1:N, n(t_10,1:N),'-o', 1:N, n(t_50,1:N),'-o', 1:N, n(end,1:N),'-o')
        %1:N, n(t_1000,1:N),'-o', 1:N, n(t_10000,1:N),'-o', 1:N, n(t_20000,1:N),'-o', 1:N, n(end,1:N),'-o')
    ylim([0 0.2])
    xlabel('Size of cluster') 
    ylabel('Average number of clusters') 
    legend('t = 0','t = 10', 't = 50', 't = 1000', 't = 10000', 't = 20000', 't = end', location = 'north')
    f = gcf;
    exportgraphics(f,'graph_high_res.png','Resolution',600);
    %figure(3)
    %tmin = tspan(1);
    %tmax = tspan(2);
    %t_len = length(t);
    %t_step = (tmax-tmin)/t_len;
    %t_list = tmin:t_step:tmax-t_step;
    %tlen = length(t_list);
    %x = 1:N;

    %for j = 1
        %y = n(j,1:N);
        %plot(x,y);
        %ylim([0 10])
        %gif('clustersize.gif','overwrite',true);
    %end
    %for j = 2:tlen
        %y = n(j,1:N);
        %plot(x,y);
        %ylim([0 10]);
        %gif;
    %end

    %figure(4)
    %plot(t, derivative_norm)
   

    %figure(5)
    %plot(1:N, n(t_1000,1:N),'-o', 1:N, n(t_10000,1:N),'-o', 1:N, n(end,1:N),'-o')
    %ylim([0 0.3])
    %xlabel('Size of cluster') 
    %ylabel('Number of clusters') 
    %legend('t = 1000', 't = 10000', 't = end', location = 'north')
    %f = gcf;
    %exportgraphics(f,'two_parameter_graph_high_res.png','Resolution',600);


    figure(6)
    bar(1:N, n(end,1:N))
    ylim([0 0.45])
    xlim([0 100])
    xlabel('Size of cluster') 
    ylabel('Number of clusters') 
    %legend('t = 1000', 't = 10000', 't = end', location = 'north')
    f = gcf;
    exportgraphics(f,'bar.png','Resolution',600);


    figure(7)
    loglog(t,derivative_l2_norm)
    xlabel('time') 
    ylabel('l2 norm of derivatives') 
end