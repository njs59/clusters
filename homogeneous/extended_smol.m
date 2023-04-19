% N = 100;
% gamma = 0;
% alpha = 1;
% V = 1;
% beta = 100000; % Large beta reduces exit from region
% m = 0.2;
% d = 0.01;

% b = 0.01;
% s = 0.01;
% r = 0.01;

%Initial condition of a single cluster of size 1
N = 100;
%n0 = ones(1,N);
%n0(N) = 0;

% Metastatic invasion IC
n0 = zeros(1,2*N);
n0(1:100) = 1;
% n0(1) = 1000;
tmin = 0;
tmax = 100;
tspan = [tmin tmax];

[t,n] = ode45(@ext_smol, tspan, n0);

output_statistics = sum_totals(n,t);

population_plots(n,t,tspan);

function [dni_dt, meta] = rhs_i(i,n,t)
N = 100;
gamma = 0;
alpha = 1;
V = 1;
beta = 100000; % Large beta reduces exit from region
m = 0.9;
d = 0.01;
    % Function inputs:
    % i integer, size of cluster
    % n vector of length N, previous distribution of cluster sizes
    % t value, time

    %Flux term is entry of cells to region - exit of cells from region
    flux = gamma/(alpha*V) - n(i)/beta;
    
    % Coagulation term calculation
    coagulation = cell_coagulation(n,i,t,N);
    
    % lifespan term is mitosis + death
    lifespan = cell_lifespan(n,i,N,m);
    
    % Now call the cell splitting function
    split = cluster_splitting(n,i,t,N);
    
    metastatic = metastatic_invasion(n,i,N);

    % Output is the sum of these terms
    dni_dt = flux + coagulation + lifespan +  split - metastatic;
    meta = metastatic;
end

function dn_dt = ext_smol(t,n0)
N = 100;
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
