function [lifespan] = cell_proliferation(n,i,N,m)
    if i == 1
        mitosis = -1*m*n(i);
    elseif i == 100
    %elseif i == N
        mitosis = m*(n(i-1)-n(i));
    else
        mitosis = m*(n(i-1)-n(i));
    end
    lifespan = mitosis;
end