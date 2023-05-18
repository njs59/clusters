function coagulation = cell_coagulation(n,i,b,t,N)
    function out = B_ij(i,j,b,scaling,t)
        % Need very small b constant
        %b = 0.00000001;
        % b = 0.01;
        %D_i = 1/i;
        %D_j = 1/j;
        %out = b*(1/scaling)*(1/(D_i+D_j));
        out = b*(1/scaling)*i*j;
        %out = b*1;
    end

% Coagulation term calculation
    %scaling = (floor(N/2)*ceil(N/2))/(floor(N/2)+ceil(N/2));
    scaling = N*N;
    
    % 1st sum of coagulation term calculation
    sum1 = 0;
    if i == 1
        sum1 = 0;
    else
        for j = 1:i-1
            sum1 = sum1 + B_ij((i-j),j,b,scaling,t)*n(i-j)*n(j);
        end
    end

    % 2nd sum of coagulation term calculation
    sum2 = 0;
    %for j = 1:i-1
    %        sum2 = sum2 + B_ij(i,j,t)*n(i)*n(j);
    %end
    %for j = i
    %    sum2 = sum2 + B_ij(i,j,t)*n(i)*(n(i)-1);
    %end
    %for j = i+1:N-i
    %    sum2 = sum2 + B_ij(i,j,t)*n(i)*n(j);
    %end
    for j = 1:N-i
        sum2 = sum2 + B_ij(i,j,b,scaling,t)*n(i)*n(j);
    end
coagulation = (1/2)*sum1 - sum2;
end