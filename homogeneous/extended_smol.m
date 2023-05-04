global N
N = 10;

global q
q = 0.01;

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

global m
m = 0;
% m = 0.9;
global d
d = 0;
% d = 0.01

%Write 1 for shedding and 0 for splitting
global shed_or_split
shed_or_split = 1;

%Initial condition of a single cluster of size 1
%n0 = ones(1,N);
%n0(N) = 0;

% Metastatic invasion IC
n0 = zeros(1,2*N);
n0(1:N) = 1;
% n0(1) = 1000;
tmin = 0;
tmax = 100;
tspan = [tmin tmax];

[t,n] = ode45(@ext_smol, tspan, n0);

save('array_n.mat','n')
save('array_t.mat','t')

output_statistics = sum_totals(n,t);

population_plots(n,t,tspan)

% population_plots2(n,t,tspan)

function [dni_dt, meta] = rhs_i(i,n,t)
global N
global m
global d
global q

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
    coagulation = cell_coagulation(n,i,t,N);
    
    % lifespan term is mitosis + death
    lifespan = cell_lifespan(n,i,N,m);
    %fprintf('Lifespan is');  % Method 1
    %disp(lifespan)
    % Now call the cell splitting function
    if shed_or_split == 0
        shed_split = cluster_splitting(n,i,t,N);
    elseif shed_or_split == 1
            if i == 1
                shed_1_sum = 0;
                for j = 2:N
                    shed_1_sum = shed_1_sum + cluster_shedding(n,j,t);
                end
                shed_split = shed_1_sum;
            elseif i == N
                shed_split = -cluster_shedding(n,i,t);
            else
                shed_split = cluster_shedding(n,i+1,t) - cluster_shedding(n,i,t);
            end
    end
    
    metastatic = metastatic_invasion(n,i,N);

    % Output is the sum of these terms
    dni_dt = flux + coagulation + lifespan +  shed_split - metastatic;
    meta = metastatic;
end

function dn_dt = ext_smol(t,n0)
global N
mu = 0.0001;
% Evaluates the RHS of all N equations that form the RHS of the system
dn_dt = zeros(N+1,1);

%n = zeros(N,length(tspan));
%n(0,:) = n0;

    for i = 1:N
        % dn_dt(i) = rhs_i(i,n(i,:),t);
        [dn_dt(i), metastatic] = rhs_i(i,n0,t);
        dn_dt(N+i) = metastatic;
    end

end
