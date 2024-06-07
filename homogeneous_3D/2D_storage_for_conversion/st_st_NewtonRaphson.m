%Function NewtonRaphson_nl() is given below.
global N
N=100;
global M
M=100;

fn = @rhs;
jacob_fn = zeros(N,1);
jacob_fn(1) = M;
error = 10^-5 ;
v = zeros(N,1);
v(1) = M;
no_itr = 20 ;
[point,no_itr,error_out]=NewtonRaphson_nl(v,fn,jacob_fn,no_itr,error)
%NewtonRaphson_nl_print(v,fn,jacob_fn,no_itr,error);





bar(1:N, point)

function F = rhs(x)
    lam = 0.1;
    global N
    global M
    cap = min(N,M);
    %% Calculation for clusters of size 1
    sum_1 = 0;
    sum_2 = 0;
    for j = 1:cap-1
        sum_1 = sum_1 + -2*x(1)*x(j);
    end
    coag_1 = sum_1 + sum_2;

    sum_3 = 0;
    for j = 2:cap
        sum_3 = sum_3 + 2*lam*x(j);
    end
    shed_1 = 2*lam*x(2) + sum_3;

    F(1) = coag_1 + shed_1;
    %% Calculation for non-extremal cluster sizes
    for i = 2:cap-1
        sum_1 = 0;
        sum_2 = 0;
        for j = 1:cap-i
            sum_1 = sum_1 + -2*x(i)*x(j);
        end
        for m = 1:i-1
            n = i-m;
            sum_2 = sum_2 + x(m)*x(n);
        end
        coag_i = sum_1 + sum_2;


        shed_i = 2*lam*(x(i+1) - x(i));

        F(i) = coag_i + shed_i;
    end
    %% Calculation for max cluster size
    sum_1 = 0;
    sum_2 = 0;
    for m = 1:cap-1
        n = cap-m;
        sum_2 = sum_2 + x(m)*x(n);
    end
    coag_cap = sum_1 + sum_2;
    shed_cap = -2*lam*x(cap);

    F(cap) = coag_cap + shed_cap;
    %% Calculation for algebraic expression
    M_star = M;
    alg_sum = 0;
    for i = 1:cap
        alg_sum = alg_sum + i*x(i);
    end
    F(cap+1) = alg_sum - M_star;
end

function dF = Jac_RHS(x)
    lam = 0.1;
    global N
    global M
    cap = min(N,M);
    %% Calculation for clusters of size 1
    sum_1 = 0;
    sum_2 = 0;
    for j = 1:cap-1
        sum_1 = sum_1 + -2*x(1)*x(j);
    end
    coag_1 = sum_1 + sum_2;

    sum_3 = 0;
    for j = 2:cap
        sum_3 = sum_3 + 2*lam*x(j);
    end
    shed_1 = 2*lam*x(2) + sum_3;

    F(1) = coag_1 + shed_1;
    %% Calculation for non-extremal cluster sizes
    for i = 2:cap-1
        sum_1 = 0;
        sum_2 = 0;
        for j = 1:cap-i
            sum_1 = sum_1 + -2*x(i)*x(j);
        end
        for m = 1:i-1
            n = i-m;
            sum_2 = sum_2 + x(m)*x(n);
        end
        coag_i = sum_1 + sum_2;


        shed_i = 2*lam*(x(i+1) - x(i));

        F(i) = coag_i + shed_i;
    end
    %% Calculation for max cluster size
    sum_1 = 0;
    sum_2 = 0;
    for m = 1:cap-1
        n = cap-m;
        sum_2 = sum_2 + x(m)*x(n);
    end
    coag_cap = sum_1 + sum_2;
    shed_cap = -2*lam*x(cap);

    F(cap) = coag_cap + shed_cap;
    %% Calculation for algebraic expression
    M_star = M;
    alg_sum = 0;
    for i = 1:cap
        alg_sum = alg_sum + i*x(i);
    end
    F(cap+1) = alg_sum - M_star;
end















function [v1 , no_itr, norm1] = NewtonRaphson_nl(v,fn,jacob_fn,no_itr,error)
    % nargin = no. of input arguments
    if nargin <5 , no_itr = 20 ; end
    if nargin <4 , error = 10^-5;no_itr = 20 ; end
    if nargin <3 ,no_itr = 20;error = 10^-5; v = [1;1;1]; end
    
    v1 = v;
    fnv1 = feval(fn,v1);
    i = 0;
    while true
        jacob_fnv1 = feval(jacob_fn,v1);
        H = jacob_fnv1\fnv1;
        v1 = v1 - H;
        fnv1 = feval(fn,v1);
        i = i + 1 ;
        norm1 = norm(fnv1);
        if i > no_itr && norm1 < error, break , end
        %if norm(fnv1) < error , break , end
    end
end
function [v1 , no_itr, norm1] = NewtonRaphson_nl_print(v,fn,jacob_fn,no_itr,error)
    v1 = v;
    fnv1 = feval(fn,v1);
    i = 0;
    fprintf('      Iteration|    x     |     y      |    z      | Error      | \n')
    while true
        norm1 = norm(fnv1);
        fprintf('%10d     |%10.4f| %10.4f | %10.4f| %10.4d |\n',i,v1(1),v1(2),v1(3),norm1)
        jacob_fnv1 = feval(jacob_fn,v1);
        H = jacob_fnv1\fnv1;
        v1 = v1 - H;
        fnv1 = feval(fn,v1);
        i = i + 1 ;
        norm1 = norm(fnv1);
        if i > no_itr && norm1 < error, break , end
        %if norm(fnv1) < error , break , end
        
    end
end