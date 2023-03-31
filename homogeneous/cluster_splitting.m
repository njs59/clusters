function split = cluster_splitting(n,i,t,N)

    function out = S_i(i,t)
        s = 0.01;
        out = s*1;
        % out = 1;
    end

    function out = r_ijk(i,j,k,t)
        if j + k == i
            out = 1/floor(i/2); %Start with constant distribution
            % 1/(i/2) if i even
            % 1/((i-1)/2) if i odd
            % We currently postulate even chance
            % of each possible splitting
        else
            disp('Inputs wrong: i + j should = k for r function')
        end
    end

split_sum = 0;
    for j = i+1:N
        split_sum = split_sum + S_i(i,t)*r_ijk(j,i,j-i,t)*n(j);
    end
    % split_sum = symsum(S_i(i,t)*r_ijk(k,i,k-i,t)*n(k),k,i+1,N);
split = split_sum - S_i(i,t)*n(i);
end