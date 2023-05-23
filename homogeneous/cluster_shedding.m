function shed = cluster_shedding(n,i,q,t)
% Function to determine the power of shedding
    function out = S_i(i,q,t)
        %global q
        s = 1;
        %s = exp(i*0.01)/q_scaling;
        out = s*q;
        % out = 1;
    end
    %shed = S_i(i,q,t)*n(i);
    shed = q*n(i);
end