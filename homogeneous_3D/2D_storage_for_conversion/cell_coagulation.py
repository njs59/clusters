def cell_coagulation(n,i,b,t,N_t,N):

## Coagulation term calculation
    # scaling = (floor(N/2)+ceil(N/2))/(floor(N/2)*ceil(N/2)); %Scaling for diffusion kernel
    # scaling = floor(N/2)*ceil(N/2); %Scaling for multiplicative kernel
    scaling = 1
    if i > N_t:
        coagulation_sum = 0
    else:
        # 1st sum of coagulation term calculation
        sum1 = 0
        if i == 0:
            sum1 = 0
        # Is this and line 21 N or N_t?
        elif i <= N-1:
        # elif i <= N:
            for j in range(0,i):
                sum1 += B_ij((i-j),j,b,scaling,t)*n[i-j-1]*n[j]
                # sum1 += B_ij((i-j),j,b,scaling,t)*n[i-j]*n[j]

        if i == N_t:
            sum2 = 0
        else:
            # 2nd sum of coagulation term calculation
            sum2 = 0
            for j in range(0,min(N-i,N_t-i)-1):
                sum2 += B_ij(i,j,b,scaling,t)*n[i]*n[j]
        
        coagulation_sum = (1/2)*sum1 - sum2


    coagulation = coagulation_sum
    return coagulation

def B_ij(i,j,b,scaling,t):
    # Need very small b constant
    # WLOG b = 1
    # D_i = 1/i
    # D_j = 1/j
    # out = b*(1/scaling)*(D_i+D_j)
    # out = b*(1/scaling)*i*j
    out = b*1
    
    return out