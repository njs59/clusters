function coagulation = cell_coagulation(n,i,b,t,N_t,N)
    function out = B_ij(i,j,b,scaling,t)
        % Need very small b constant
        % WLOG b = 1
        %D_i = 1/i;
        %D_j = 1/j;
        %out = b*(1/scaling)*(D_i+D_j);
        %out = b*(1/scaling)*i*j;
        out = b*1;
    end

% Coagulation term calculation
    %scaling = (floor(N/2)+ceil(N/2))/(floor(N/2)*ceil(N/2)); %Scaling for diffusion kernel
    %scaling = floor(N/2)*ceil(N/2); %Scaling for multiplicative kernel
    scaling = 1;
    %if i == 11
    %    disp('Hit!')
    %end
    if i > N_t
        coagulation_sum = 0;
    else
        % 1st sum of coagulation term calculation
        sum1 = 0;
        if i == 1
            sum1 = 0;
        %elseif i <= 100
        elseif i <= 100
            for j = 1:i-1
                sum1 = sum1 + B_ij((i-j),j,b,scaling,t)*n(i-j)*n(j);
            end
        end

        if i == N_t
            sum2 = 0;
        else
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
            %for j = 1:min(N-i,N_t-i)
            for j = 1:min(100-i,N_t-i)
                sum2 = sum2 + B_ij(i,j,b,scaling,t)*n(i)*n(j);
            end
        end
        coagulation_sum = (1/2)*sum1 - sum2;
    end
    %if i == 11 && coagulation_sum > 0 
        %disp('Hit!')
    %end
    coagulation = coagulation_sum;
end