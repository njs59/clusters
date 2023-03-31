function death_factor = cell_death(n,i,N)
    x = 1:100;
    d_an = geopdf(x,0.1);
    d_ap = geopdf(100-x,0.1);
    if i == N
        death_larger = 0;
        death_i = (d_an(i) + d_ap(i))*n(i);
    else
        death_larger = (d_an(i+1) + d_ap(i+1))*n(i+1);
        death_i = (d_an(i) + d_ap(i))*n(i);
    end
    death_factor = death_larger - death_i;
end