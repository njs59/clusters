global N
N=100;
global M
M=10;

fun = @rhs;
x0 = zeros(N,1);
x0(1) = M;

options = optimset('TolFun',1e-16);
x = fsolve(fun,x0,options)
bar(1:N, x)

function F = rhs(x)
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

    F(1) = coag_1;
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

        F(i) = coag_i;
    end
    %% Calculation for max cluster size
    sum_1 = 0;
    sum_2 = 0;
    for m = 1:cap-1
        n = cap-m;
        sum_2 = sum_2 + x(m)*x(n);
    end
    coag_cap = sum_1 + sum_2;

    F(cap) = coag_cap;
    %% Calculation for algebraic expression
    M_star = M;
    alg_sum = 0;
    for i = 1:cap
        alg_sum = alg_sum + i*x(i);
    end
    F(cap+1) = alg_sum - M_star;
end