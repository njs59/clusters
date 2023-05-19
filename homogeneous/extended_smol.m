%% Set-up
global N
N = 100;

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
    gamma = 0;
    alpha = 1;
    V = 1;
    beta = 100000; % Large beta reduces exit from region
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
shed_or_split = 1;

%Initial condition of a single cluster of size 1
%n0 = ones(1,N);
%n0(N) = 0;

%% IC 
% (set to allow for metastatic invasion)
n0 = zeros(1,2*N);
%n0(1:N) = 1;
n0(1) = 100;

%% Running of solver
tmin = 0;
tmax = 1000;
tspan = [tmin tmax];

[t,n] = ode45(@ext_smol, tspan, n0);

%% Outputs
derivatives = zeros(length(t),N);
derivative_l2_norm = zeros(length(t),1);
for i = 1:length(t)
    derivatives = ext_smol(t(i), n(i,1:N));
    derivative_l2_norm(i) = norm(derivatives,2);
end


%save('array_n.mat','n')
%save('array_t_0.0001.mat','t')
%save('array_norms_0.0001.mat', 'derivative_l2_norm')

output_statistics = sum_totals(n,t);

population_plots(n,t,tspan, derivative_l2_norm)

% population_plots2(n,t,tspan)


%% Functions
function [dni_dt, meta] = rhs_i(i,n,t)
global N
% global m
% global d
% global q
b = 1;
lambda = 0;
q = lambda/b;
%tau = tau + 1;
N_t = 0;
N_t_before = 0;
%if t > 0.3884
%    disp('Break');
%end
for l = 1:N
    N_t_before = l*n(l)+ N_t_before;
end
N_t = round(N_t_before);
%if N_t > 10.1
%    disp('problem!');
%end


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
    m = 0;
    d = 0;
    if m == 0 && d == 0 
        lifespan = 0;
    else
        lifespan = cell_lifespan(n,i,N,m);
    end
    %fprintf('Lifespan is');  % Method 1
    %disp(lifespan)
    % Now call the cell splitting function
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
mu = 0.0001;
% Evaluates the RHS of all N equations that form the RHS of the system
dn_dt = zeros(N+1,1);

%n = zeros(N,length(tspan));
%n(0,:) = n0;
    sum_dn_dt = 0;
    %tau = 0;
    for i = 1:N
        % dn_dt(i) = rhs_i(i,n(i,:),t);
        [dn_dt(i), metastatic] = rhs_i(i,n0,t);
        dn_dt(N+i) = metastatic;
        sum_dn_dt = sum_dn_dt + dn_dt(i);
    end
end
