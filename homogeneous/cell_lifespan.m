function [lifespan] = cell_lifespan(n,i,N,m)
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
end