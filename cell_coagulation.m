function coagulation = cell_coagulation(n,i,t,N)

    function out = B_ij(i,j,t)
        b = 0.0001;
        out = b*1;
        % out = 1;
    end

% Coagulation term calculation
    
    % 1st sum of coagulation term calculation
    sum1 = 0;
    if i == 1
        sum1 = 0;
    else
        for j = 1:i-1
            sum1 = sum1 + B_ij(i,j,t)*n(i-j)*n(j);
        end
    end

    % 2nd sum of coagulation term calculation
    sum2 = 0;
    for j = 1:N
            sum2 = sum2 + B_ij(i,j,t)*n(i)*n(j);
    end
coagulation = (1/2)*sum1 - sum2;
end