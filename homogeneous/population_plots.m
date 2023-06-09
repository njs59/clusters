function [] = population_plots(n,t,tspan, derivative_l2_norm, n_change)
    global N
    figure(1)
    plot(t,n(:,1), t,n(:,2), t,n(:,3), t,n(:,5), t,n(:,10))
    xlabel('time') 
    ylabel('Number of clusters')
    xlim([0 0.2])
    ylim([0 40])
    legend('n=1', 'n=2', 'n=3', 'n=5', 'n=10')
    f = gcf;
    exportgraphics(f,'individual_cluster_size.png','Resolution',600);


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
    ylim([0 2])
    xlim([0 100])
    xlabel('Size of cluster') 
    ylabel('Number of clusters') 
    %legend('t = 1000', 't = 10000', 't = end', location = 'north')
    f = gcf;
    exportgraphics(f,'bar.png','Resolution',600);


    %figure(7)
    %loglog(t,derivative_l2_norm)
    %xlabel('time') 
    %ylabel('l2 norm of derivatives') 

    %figure(8)
    %t_after = t(2:end);
    %loglog(t_after,n_change)

    figure(9)
    psi_end = n(end,1:N);
    psi_end_sum = sum(psi_end);
    psi_end_normed = psi_end/psi_end_sum;
    bar(1:N, psi_end_normed)
    ylim([0 0.06])
    xlim([0 100])
    xlabel('Size of cluster') 
    ylabel('Normed proportion of clusters') 
    %legend('t = 1000', 't = 10000', 't = end', location = 'north')
    f = gcf;
    exportgraphics(f,'normed_bar.png','Resolution',600);
end