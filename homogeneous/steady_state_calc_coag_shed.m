global N
N=100;
global M
M=100;

fun = @rhs;
x0 = zeros(N,1);
x0(1) = M;

options = optimset('TolFun',1e-8);
x = fsolve(fun,x0)
bar(1:N, x)

function F = rhs(x)
    global N
    global M
    lam = 1;
    b = 1;
    %scaling = 1;
    %scaling = (floor(N/2)*ceil(N/2))/(floor(N/2)+ceil(N/2)); %Scaling for diffusion kernel
    %scaling = floor(N/2)*ceil(N/2); %Scaling for multiplicative kernel
    scaling = calc_scaling(N,1); % 1 for cst, 2 for diff, 3 for mult
    cap = min(N,M);
    %% Calculation for clusters of size 1
    sum_1 = 0;
    sum_2 = 0;
    for j = 1:cap-1
        sum_1 = sum_1 + -B_ij(1,j,b,scaling)*x(1)*x(j);
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
            sum_1 = sum_1 + -B_ij(i,j,b,scaling)*x(i)*x(j);
        end
        for m = 1:i-1
            n = i-m;
            sum_2 = sum_2 + (1/2)*B_ij(m,n,b,scaling)*x(m)*x(n);
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
        sum_2 = sum_2 + (1/2)*B_ij(m,n,b,scaling)*x(m)*x(n);
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

function out = B_ij(i,j,b,scaling)
    % Need very small b constant
    % WLOG b = 1
    %D_i = 1/i;
    %D_j = 1/j;
    %out = b*(1/scaling)*(1/(D_i+D_j));
    %out = b*(1/scaling)*i*j;
    out = b*2;
end

function scaling_factor = calc_scaling(N,selection)
    scaling_factor_sum = 0;
    for i = 1:N
        for j = 1:N
            if selection == 1
                scaling_factor_sum = scaling_factor_sum + 1; %Cst Kernel
            elseif selection == 2
                scaling_factor_sum = scaling_factor_sum + (i*j)/(i+j); %Diffusion kernel
            elseif selection == 3
                scaling_factor_sum = scaling_factor_sum + i*j; %Mult kernel
            end
        end
    end
    scaling_factor = N*N/scaling_factor_sum;
end


