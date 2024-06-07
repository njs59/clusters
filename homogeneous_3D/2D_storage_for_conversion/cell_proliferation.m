function [lifespan] = cell_proliferation(n,i,N,m)
    if i == 1
        mitosis = -1*2*sqrt(i)*m*n(i);
    elseif i == 100
    %elseif i == N
        % mitosis = m*(2*sqrt(i-1)*n(i-1)-2*sqrt(i)*n(i));
        mitosis = m*(2*sqrt(i-1)*n(i-1));
    else
        mitosis = m*(2*sqrt(i-1)*n(i-1)-2*sqrt(i)*n(i));
    end
    lifespan = mitosis;
end