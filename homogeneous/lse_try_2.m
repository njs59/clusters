n_st = load('b_0.0005_m_0_n_arr.mat');
t_st = load('b_0.0005_m_0_t_arr.mat');

n_out = n_st.n.';
t_span = t_st.t;

b = optimvar('b',1,"LowerBound",0.0001,"UpperBound",1);

global N
N = 500;

n0 = zeros(1,N);
n0(1) = 500;

%type extended_smol.m
%type btoODE

myfcn = fcn2optimexpr(@btoODE,t_span,n0,b);

obj = sum(sum((myfcn - n_out).^2));

prob = optimproblem("Objective",obj);


b0.b = 0.0001;
[bsol,sumsq] = solve(prob,b0)
disp(bsol.b)




noise_par = 0.25;
n_noisy = n_out .* (1 + noise_par * normrnd(0,1,size(n_out)));


obj_noisy = sum(sum((myfcn - n_noisy).^2));
prob_noisy = optimproblem("Objective",obj_noisy);


final_row = tail(n_noisy.',1);
plot(final_row(1:100))

b0_noisy.b = 0.0001;
[bsol_noisy,sumsq_noisy] = solve(prob_noisy,b0_noisy)
disp(bsol_noisy.b)

% obj2 = @(b)ext_smol(t,n,b,t_span,n0);
% results = bayesopt(obj,[b,n0])


function solpts = btoODE(t_span,n0,b)
    sol = ode45(@(t,n)ext_smol(t,n,b),t_span,n0);
    solpts = deval(sol,t_span);
end


%% Functions
function [dni_dt] = rhs_i(i,n,t, b)
global N

N_t = 0;
N_t_before = 0;

for l = 1:N
    N_t_before = l*n(l)+ N_t_before;
end
N_t = round(N_t_before);
    % Coagulation term calculation
    coagulation = cell_coagulation(n,i,b,t,N_t,N);
    
    % lifespan term is mitosis + death
    m = 0;
    d = 0;
    if m == 0 && d == 0 
        lifespan = 0;
    else
        % lifespan = cell_lifespan(n,i,N,m);
        lifespan = cell_proliferation(n,i,N,m);
    end
    dni_dt = coagulation + lifespan;
end


function [dn_dt]  = ext_smol(t,n0, b)
global N
% Evaluates the RHS of all N equations that form the RHS of the system
dn_dt = zeros(N,1);

    sum_dn_dt = 0;
    for i = 1:N
        dn_dt(i) = rhs_i(i,n0,t, b);
    end
    if sum_dn_dt < 1e-6
        return
    end
end
