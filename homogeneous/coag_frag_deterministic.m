%% Set-up
global N
N = 100;

%global q
%q = 0.01;


%Write 1 for shedding and 0 for splitting
global shed_or_split
shed_or_split = 1;

%Initial condition of a single cluster of size 1
%n0 = ones(1,N);
%n0(N) = 0;

%% IC 
% (set to allow for metastatic invasion)
%n0 = zeros(1,2*N);
n0 = zeros(1,N);
%n0(1:N) = 1;
global M
M = 120;
n0(1) = M;

%% Running of solver
tmin = 0;
tmax = 100000;
tstep = 1;
tspan = [tmin tmax];

%[t,n] = ode45(@ext_smol, tspan, n0);
n = zeros(tmax+1, N);
t = tmin:tmax;
t_num_steps = tmax - tmin;
n(1,:) = n0;

n_change = zeros(1,t_num_steps);

for t_current_step = 1:t_num_steps
    n_before = n(t_current_step,:);
    n_change_current = 0;
    for i = 1:N
        step_change = rhs_i(i,n_before,t);
        n(t_current_step + 1, i) = n(t_current_step, i) + step_change;
        n_change_current = n_change_current + norm(step_change);
    end
    n_change(t_current_step) = n_change_current;
end


%% Outputs
%derivatives = zeros(length(t),N);
%derivative_l2_norm = zeros(length(t),1);
%for i = 1:length(t)
%    derivatives = ext_smol(t(i), n(i,1:N));
%    derivative_l2_norm(i) = norm(derivatives,2);
%end


%save('array_n.mat','n')
%save('array_t_0.0001.mat','t')
%save('array_norms_0.0001.mat', 'derivative_l2_norm')

output_statistics = sum_totals(n,t);

population_plots(n,t,tspan, derivative_l2_norm, n_change)

% population_plots2(n,t,tspan)


%% Functions
function [dni_dt] = rhs_i(i,n,t)
global N
global M
global shed_or_split
b = 0.1/(M); %Chance of success, rate of reaction
lambda = 0.1;
q = lambda*b;
%scaling_q = 0;
%for l = 1:100
%    scaling_q = scaling_q + exp(i*0.01);
%end

N_t = 0;
N_t_before = 0;

for l = 1:N
    N_t_before = l*n(l)+ N_t_before;
end
N_t = round(N_t_before);


    
    % Coagulation term calculation
    coagulation = cell_coagulation(n,i,b,t,N_t,N);
    
    if shed_or_split == 0
        shed_split = cluster_splitting(n,i,t,N);
    elseif shed_or_split == 1
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
    
%    is_metastatic = false;
%    if is_metastatic == false
%        metastatic = 0;
%    else
%        metastatic = metastatic_invasion(n,i,N);
%    end
    
    dni_dt = coagulation +  shed_split;
    %dni_dt = coagulation +  shed_split - metastatic;
%    meta = metastatic;
end


function [dni_dt] = rhs_i_adapted(i,n,t)
global N
global M
global shed_or_split
b = 0.1/(M); %Chance of success, rate of reaction
lambda = 0;
q = lambda/b;
%scaling_q = 0;
%for l = 1:100
%    scaling_q = scaling_q + exp(i*0.01);
%end

N_t = 0;
N_t_before = 0;

for l = 1:N
    N_t_before = l*n(l)+ N_t_before;
end
N_t = round(N_t_before);


    
    % Coagulation term calculation
    coagulation = cell_coagulation(n,i,b,t,N_t,N);
    
    if shed_or_split == 0
        shed_split = cluster_splitting(n,i,t,N);
    elseif shed_or_split == 1
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
    
%    is_metastatic = false;
%    if is_metastatic == false
%        metastatic = 0;
%    else
%        metastatic = metastatic_invasion(n,i,N);
%    end
    
    dni_dt = coagulation +  shed_split;
    %dni_dt = coagulation +  shed_split - metastatic;
%    meta = metastatic;
end

