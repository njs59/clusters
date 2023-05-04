% Script for running 

%Initial condition of a single cluster of size 1
N = 100;
n0 = zeros(N,N);
n0(1,:) = 1;
tmin = 0;
tmax = 100;
tspan = [tmin tmax];

%Give value of 1 for shedding or 0 for splitting
shed_or_split = 1;


[t,n] = ode45(@ext_smol, tspan, n0);
figure(1)
plot(t,n(:,1), t, n(:,2))
xlabel('time') 
ylabel('Number of clusters') 
legend('n=1', 'n=2')

figure(2)
plot(1:N, n(1,:), '-o', 1:N, n(40,:),'-o', 1:N, n(end,:),'-o')
xlabel('Size of cluster') 
ylabel('Number of clusters') 
legend('t=0','t = mid', 't=10')

figure(3)
tspan = [tmin tmax];
t_len = length(t);
t_step = (tmax-tmin)/t_len;

t_list = tmin:t_step:tmax-t_step;
% p = plot(nan,nan);
% p.XData = x;
tlen = length(t_list);
x = 1:N;
for j = 1:tlen

    % p.YData = n(y,:);
    y = n(j,:);
    plot(x,y);
    exportgraphics(gcf,'testAnimated2.gif','Append',true);
end

function dphi_ij_dt = rhs_ij(i,j,n,t)
N = 100;
gamma = 0;
alpha = 1;
V = 1;
beta = 100000; % Large beta reduces exit from region
m = 0.9;
d = 0.01;
q= 0.01;
    % Function inputs:
    % i integer, size of cluster
    % n vector of length N, previous distribution of cluster sizes
    % t value, time

    %Flux term is entry of cells to region - exit of cells from region
    flux = gamma/(alpha*V) - n(i)/beta;
    
    % Coagulation term calculation
    coagulation = cell_coagulation(n,i,j,t,N);
    
    % lifespan term is mitosis + death
    if i == 1
        mitosis = -1*m*n(i);
        % death = d*(n(i+1)-n(i));
        death = cell_death(n,i,j,N);
    elseif i == N
        mitosis = m*(n(i-1)-n(i));
        % death = -1*d*n(i);
        death = cell_death(n,i,N);
    else
        mitosis = m*(n(i-1)-n(i));
        death = cell_death(n,i,N);
    end
    lifespan = mitosis + death;
    
    % Now call the cell splitting function
    if shed_or_split == 0
        shed_split = cluster_splitting(n,i,t,N);
    elseif shed_or_split == 1
            if i == 1
                shed_1_sum = 0;
                for j = 2:N
                    shed_1_sum = shed_1_sum + cluster_shedding(n,j,q,t);
                end
                shed_split = shed_1_sum;
            else
                shed_split = cluster_shedding(n,i+1,t) - cluster_shedding(n,i,q,t);
            end
    end

    % Output is the sum of these terms
    dphi_ij_dt = flux + coagulation + lifespan +  shed_split;
end

function dn_dt = ext_smol(t,n0)
N = 100;

% Evaluates the RHS of all N equations that form the RHS of the system
dn_dt = zeros(N,1);

%n = zeros(N,length(tspan));
%n(0,:) = n0;
    for i = 1:N
        % dn_dt(i) = rhs_i(i,n(i,:),t);
        dn_dt(i) = rhs_i(i,n0,t);
    end
end