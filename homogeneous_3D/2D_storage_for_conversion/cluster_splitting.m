function split = cluster_splitting(n,i,t,N)

    function out = S_i(i,t)
        s = 0.0001;
        out = s*1;
        % out = 1;
    end

    function out = r_ijk(i,j,k,t)
        if j + k == i
            out = 1/floor(i/2); %Start with constant distribution
            % out = 1;
            % 1/(i/2) if i even
            % 1/((i-1)/2) if i odd
            % We currently postulate even chance
            % of each possible splitting
        else
            disp('Inputs wrong: i + j should = k for r function')
        end
    end

split_gain = 0;
split_loss = 0;
    if i < N/2 % If smaller than half max size then a split into 2 of same size exists
        for j = i+1:(2*i)-1
            split_gain = split_gain + S_i(i,t)*r_ijk(j,i,j-i,t)*n(j);
        end
        for j = 2*i
            split_gain = split_gain + 2*S_i(i,t)*r_ijk(j,i,j-i,t)*n(j);
        end
        for j = 2*i+1:N
            split_gain = split_gain + S_i(i,t)*r_ijk(j,i,j-i,t)*n(j);
        end
    else
        for j = i+1:N
            split_gain = split_gain + S_i(i,t)*r_ijk(j,i,j-i,t)*n(j);
        end
    end
    % split_sum = symsum(S_i(i,t)*r_ijk(k,i,k-i,t)*n(k),k,i+1,N);
    if i == 1
        split_loss = 0;
    else
        split_loss = S_i(i,t)*n(i);
    end
split = split_gain - split_loss;
end