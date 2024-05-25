%n_st = load('s11_inference_input_multi_well.csv');
n_st = load('s11_inference_input.csv');

n_chop = n_st(:,3:61);
n_out = n_chop.';
t_span = linspace(39,97,59);

% b = optimvar('b',"LowerBound",0.0001,"UpperBound",1);
% N = optimvar('N',"LowerBound",100,"UpperBound",10000);
% 
% b0.b = 0.0001;
% N0.N = 100;


N_t_before = zeros(59,1);
for h = 1:59
    for l = 1:100
        N_t_before(h) = l*n_out(h,l)+ N_t_before(h);
    end
end
n_out_10 = zeros(10,59);
for k = 1:59
    for i = 1:10
        for j = 1:10
            n_out_10(i,k) = n_out_10(i,k) + n_chop(10*(i-1) + j,k);
        end
    end
end



r = optimvar('r',3,"LowerBound",[0.00001 0.00001 1],"UpperBound",[1 1 10000]);
%r0.r = [0.00001 0.00001 mean(N_t_before) ];
r0.r = [0.00001 0.00001 500 ];

% global N
% N = 500;

n0 = n_out(1,:);
% n0(1) = 500;

%type extended_smol.m
%type btoODE



myfcn = fcn2optimexpr(@btoODE,t_span,n0,r);

n_out_min = n_out.';

obj = sum(sum((myfcn - n_out_10).^2));

prob = optimproblem("Objective",obj);


[rsol,sumsq] = solve(prob,r0)
%[sol, fval, exitflag, output]  = solve(prob, b0, N0)
%[bsol,sumsq] = solve(prob,b0)
disp(rsol.r)
%disp(Nsol.N)

% noise = 25;
% n_noisy = n_out + normrnd(0,25,size(n_out));
% 
% 
% obj_noisy = sum(sum((myfcn - n_noisy).^2));
% prob_noisy = optimproblem("Objective",obj_noisy);
% 
% 
% final_row = tail(n_noisy.',1);
% plot(final_row(1:100))
% 
% b0_noisy.b = 0.0001;
% [bsol_noisy,sumsq_noisy] = solve(prob_noisy,b0_noisy)
% disp(bsol_noisy.b)

% obj2 = @(b)ext_smol(t,n,b,t_span,n0);
% results = bayesopt(obj,[b,n0])


function solpts_10 = btoODE(t_span,n0,r)
    b = r(1);
    m = r(2);
    N = r(3);
    sol = ode45(@(t,n)ext_smol(t,n,b,m,N),t_span,n0);
    solpts = deval(sol,t_span);
    solpts_10 = zeros(10,length(t_span));
    for k = 1:59
        for i = 1:10
            for j = 1:10
                solpts_10(i,k) = solpts_10(i,k) + solpts(10*(i-1) + j, k);
            end
        end
    end
end


%% Functions
function [dni_dt] = rhs_i(i,n,t, b,m,N)
% global N

N_t = N;
% N_t_before = 0;

%for l = 1:100
%    N_t_before = l*n(l)+ N_t_before;
%end
%N_t = round(N_t_before);
    % Coagulation term calculation
    coagulation = cell_coagulation(n,i,b,t,N_t,N);
    
    % lifespan term is mitosis + death
    % m = 0;
    d = 0;
    if m == 0 && d == 0 
        lifespan = 0;
    else
        % lifespan = cell_lifespan(n,i,N,m);
        lifespan = cell_proliferation(n,i,N,m);
    end
    dni_dt = coagulation + lifespan;
end


function [dn_dt]  = ext_smol(t,n0, b,m,N)
% global N
% Evaluates the RHS of all N equations that form the RHS of the system
dn_dt = zeros(100,1);

    sum_dn_dt = 0;
    for i = 1:100
        dn_dt(i) = rhs_i(i,n0,t, b,m,N);
    end
    if sum_dn_dt < 1e-6
        return
    end
end
