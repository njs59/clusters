function shed = cluster_shedding(n,i,t)
% Function to determine the power of shedding
    function out = S_i(i,t)
        global q
        s = 1;
        out = s*q;
        % out = 1;
    end

    shed = S_i(i,t)*n(i);

end