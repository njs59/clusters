%% Set-up
global N
%N = 500;
N = 100;
%N = 7.13097669e+02;

global b_test
global m_test

%b_test = [0.0010, 0.0015, 0.0020, 0.0030];
%b_test = [0.0004, 0.0004, 0.0005, 0.0005];
%b_test = [0.0004];
b_test = [4.11235554e-07];
%b_test = [0.000433477336187832]

%m_test = [0, 0.1, 0, 0.1];
m_test = [0];
%m_test = [0.0280573030331480];

%global q
%q = 0.01;

global include_flux
include_flux = false;
if include_flux == false
    disp('No flux assumed');
else
    global gamma
    global alpha
    global V
    global beta
    %gamma = 0;
    %alpha = 1;
    %V = 1;
    %beta = 100000; % Large beta reduces exit from region
end

global include_flux
include_flux = false;
if include_flux == false
    disp('No flux assumed');
end

%global m
%m = 0;
% m = 0.9;
%global d
%d = 0;
% d = 0.01

%Write 1 for shedding and 0 for splitting
global shed_or_split
shed_or_split = 0;

%Initial condition of a single cluster of size 1
%n0 = ones(1,N);
%n0(N) = 0;

%% IC 
% (set to allow for metastatic invasion)
n0 = zeros(1,N);
n0(1) = 7.13097669e+02;

% n_st = load('s11_inference_input.csv');
% 
% n_chop = n_st(:,3:61);
% n_out = n_chop.';
% n0 = n_out(1,:);
% final_data_point = tail(n_out,1)

%% Running of solver
% tmin = 39;
% tmax = 97;
tmin = 0;
% tmax = 145;

tmax = 100000;
tspan = [tmin tmax];
for runs = 1:length(b_test)
    global run_number
    run_number = runs;
    [t,n] = ode45(@ext_smol, tspan, n0);
    
    %% Outputs
    derivatives = zeros(length(t),N);
    derivative_l2_norm = zeros(length(t),1);
    for i = 1:length(t)
        derivatives = ext_smol(t(i), n(i,1:100));
        %derivatives = ext_smol(t(i), n(i,1:N));
        derivative_l2_norm(i) = norm(derivatives,2);
    end
    
    
    %save('array_n.mat','n')
    %save('array_t_0.0001.mat','t')
    %save('array_norms_0.0001.mat', 'derivative_l2_norm')
    
    %output_statistics = sum_totals(n,t);
    
    % population_plots(n,t,tspan, derivative_l2_norm)
    final_row = tail(n,1);
    final_row_10 = zeros(10,1);
    for i = 1:10
        for j = 1:10
            final_row_10(i) = final_row_10(i) + final_row(10*(i-1) + j);
        end
    end
    

    %% Summary statistics
    num_clus = sum(n,2);
    tot_2D = zeros(length(t), 1);
    for i = 1:length(t)
        for j = 1:100
            tot_2D(i) = tot_2D(i) + j*n(i,j);
        end
    end

    mean_2D_size = tot_2D./num_clus;


    %% Plots
    
    x_plot = 0:10:100;
    figure(1)
    plot(final_row(1:100))

    figure(2)
    hold on
    histogram('BinEdges',x_plot,'BinCounts',final_row_10, FaceAlpha=0.5)
    %histogram('BinEdges',x_plot,'BinCounts',final_data_point, FaceAlpha=0.5)
    hold off
    legendStrings = "b = " + string(b_test) + "  m = " + string(m_test);
    legend(legendStrings)
  
    figure(3)
    hold on
    plot(t,num_clus)
    hold off
    legendStrings = "b = " + string(b_test) + "  m = " + string(m_test);
    legend(legendStrings)

    figure(4)
    hold on
    plot(t,tot_2D)
    hold off

    figure(5)
    hold on
    plot(t,mean_2D_size)
    hold off
    
    
    % population_plots2(n,t,tspan)
end

%% Functions
function [dni_dt, meta] = rhs_i(i,n,t)
global N
global run_number
global b_test
global m_test
% global m
% global d
% global q
b = b_test(run_number);
% b = 0.001;
lambda = 0;
q = lambda*b;
%scaling_q = 0;
%for l = 1:100
%    scaling_q = scaling_q + exp(i*0.01);
%end

N_t = 0;
N_t_before = 0;
%for l = 1:N
for l = 1:100
    N_t_before = l*n(l)+ N_t_before;
end
N_t = round(N_t_before);



global include_flux

global shed_or_split
    % Function inputs:
    % i integer, size of cluster
    % n vector of length N, previous distribution of cluster sizes
    % t value, time
    if include_flux == true
        global gamma
        global alpha
        global V
        global beta
        %Flux term is entry of cells to region - exit of cells from region
        flux = gamma/(alpha*V) - n(i)/beta;
    else
        flux = 0;
    end
    
    % Coagulation term calculation
    coagulation = cell_coagulation(n,i,b,t,N_t,N);
    
    % lifespan term is mitosis + death
    % m = 0.01;
    m = m_test(run_number);
    d = 0;
    if m == 0 && d == 0 
        lifespan = 0;
    else
        % lifespan = cell_lifespan(n,i,N,m);
        lifespan = cell_proliferation(n,i,N,m);
    end
    %fprintf('Lifespan is');  % Method 1
    %disp(lifespan)
    % Now call the cell splitting function
    if shed_or_split == 0
        shed_split = 0;
    elseif shed_or_split == 1
        shed_split = cluster_splitting(n,i,t,N);
    elseif shed_or_split == 2
        shed_split = 0;
            if i == 1
                shed_1_sum = cluster_shedding(n,2,q,t); %Need to count twice from cluster of size 2
                %Cluster size 2 splits into "big" 1 and "shedded" 1
                for j = 2:N
                    shed_1_sum = shed_1_sum + cluster_shedding(n,j,q,t);
                    shed_split = shed_1_sum;
                end
            elseif i == N
                shed_split = - cluster_shedding(n,i,q,t);
            else
                shed_split = cluster_shedding(n,i+1,q,t) - cluster_shedding(n,i,q,t);
            end
    end
    
    is_metastatic = false;
    if is_metastatic == false
        metastatic = 0;
    else
        metastatic = metastatic_invasion(n,i,N);
    end

    % Output is the sum of these terms
    
    %if t > 50
    %    disp('Over!');
    %end
    dni_dt = flux + coagulation + lifespan +  shed_split - metastatic;
    meta = metastatic;
end


function [dn_dt]  = ext_smol(t,n0)
global N
global run_number

mu = 0.0001;
% Evaluates the RHS of all N equations that form the RHS of the system
dn_dt = zeros(100,1);

%n = zeros(N,length(tspan));
%n(0,:) = n0;
    sum_dn_dt = 0;
    %tau = 0;
    for i = 1:100
        dn_dt(i) = rhs_i(i,n0,t);
        %[dn_dt(i), metastatic] = rhs_i(i,n0,t);
        %dn_dt(N+i) = metastatic;
        %sum_dn_dt = sum_dn_dt + dn_dt(i);
    end
    if sum_dn_dt < 1e-6
        return
    end
end
