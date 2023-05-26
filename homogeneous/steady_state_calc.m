fun = @rhs;
x0 = zeros(100,1);
x0(1) = 100;
global lambda
lambda = 0.1;
global N
N=100;
global M
M=100;
x = fsolve(fun,x0)
bar(1:N, x)

function F = rhs(x,lam)
    global lambda
    lam = lambda;
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
        for l = 1:i-1
            for m = 1:i-l
                sum_2 = sum_2 + x(l)*x(m);
            end
        end
        coag_i = sum_1 + sum_2;


        shed_i = 2*lam*(x(i+1) - x(i));

        F(i) = coag_i + shed_i;
    end
    %% Calculation for max cluster size
    sum_1 = 0;
    sum_2 = 0;
    for l = 1:i-1
        for m = 1:i-l
            sum_2 = sum_2 + x(l)*x(m);
        end
    end
    coag_cap = sum_1 + sum_2;
    shed_cap = -2*lam*x(cap);

    F(cap) = coag_cap + shed_cap;
    %% Calculation for algebraic expression
    M_star = M*lam;
    alg_sum = 0;
    for i = 1:cap
        alg_sum = alg_sum + i*x(i);
    end
    F(cap+1) = alg_sum - M_star;
end