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
tmin = 0;
tmax = 100;
tspan = [tmin tmax];

[t,n] = ode45(@ext_smol, tspan, n0);

output_statistics = sum_totals(n,t);

figure(1)
plot(t,n(:,1), t, n(:,2))
xlabel('time') 
ylabel('Number of clusters') 
legend('n=1', 'n=2')

figure(2)
plot(1:100, n(1,1:100), '-o', 1:100, n(40,1:100),'-o', 1:100, n(end,1:100),'-o')
xlabel('Size of cluster') 
ylabel('Number of clusters') 
legend('t=0','t = mid', 't=end')

figure(3)
tspan = [tmin tmax];
t_len = length(t);
t_step = (tmax-tmin)/t_len;

t_list = tmin:t_step:tmax-t_step;
 % p = plot(nan,nan);
 % p.XData = x;
tlen = length(t_list);
x = 1:100;
for j = 1:tlen

   % p.YData = n(y,:);
   y = n(j,1:100);
   plot(x,y);
   exportgraphics(gcf,'testAnimated2.gif','Append',true);
end

% figure(4)
% tspan = [tmin tmax];
% t_len = length(t);
% t_step = (tmax-tmin)/t_len;

% t_list = tmin:t_step:tmax-t_step;
% % p = plot(nan,nan);
% % p.XData = x;
% tlen = length(t_list);
% x = 1:100;
% for j = 1:tlen

    % % p.YData = n(y,:);
    % y = n(j,101:200);
    % plot(x,y);
    % exportgraphics(gcf,'testAnimated2.gif','Append',true);
% end

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
    if i == 1
        mitosis = -1*m*n(i);
        % death = d*(n(i+1)-n(i));
        death = cell_death(n,i,N);
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
    split = cluster_splitting(n,i,t,N);

%    if t > 5
%        disp('Hit')
%    end
    
    mu = 0.00001;
    metastatic = mu*n(i);

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
