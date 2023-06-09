function [output] = sum_totals(n,t)
    global N;
    n_no_metastatic = n(:,1:N);
    n = n_no_metastatic; %For ease of reading
    sz = size(n);
    row = sz(1);
    % column = sz(2);
    output = zeros(row,5);
    for tau = 1:row
    % Phi_t is total number of cluters
    % N_t is total number of cells
    % N2_t is total of squared size of clusters
        Phi_t = sum(n(tau,:));
        N_t = 0;
        N2_t = 0;
        for i = 1:N
            N_t = i*n(tau,i)+N_t;
            N2_t = (i^2)*n(tau,i)+N2_t;
        end
        mean_cluster_size = N_t/Phi_t;
        Ex_N2 = N2_t/Phi_t;
        Ex_N = mean_cluster_size;
        var_cluster_size = Ex_N2 - (Ex_N)^2;

        tot_clus_num = Phi_t;
        tot_cell_num = N_t;
        av_size = mean_cluster_size;
        var_size = var_cluster_size;
        
        output(tau,1) = t(tau); % 1st column is the time
        output(tau,2) = tot_clus_num; % 2nd column is the total number of clusters
        output(tau,3) = tot_cell_num; % 3rd column is the total number of cells
        output(tau,4) = av_size; % 4th column is the average cluster size
        output(tau,5) = var_size; % 5th column is the variance of cluster sizes

    end

end