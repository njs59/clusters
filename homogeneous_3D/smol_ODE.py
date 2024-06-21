import numpy as np
import cell_coagulation


## Functions
def rhs_i(i,n,t,b,N):
    # b = b_test[run_number]

    N_t = 0
    N_t_before = 0

    for l in range(0,N):
        N_t_before = (l+1)*n[l]+ N_t_before
    N_t = round(N_t_before)



    coagulation = cell_coagulation.cell_coagulation(n,i,b,t,N_t,N)
    
    # lifespan = cell_proliferation(n,i,N)
    dni_dt = coagulation 

    return dni_dt


def ext_smol(n0,t_curr,b,N):
    dn_dt = np.zeros(N)
    # n = n0
    sum_dn_dt = 0
    for i in range(0,N):
        dn_dt[i] = rhs_i(i,n0,t_curr,b,N)
    # if sum_dn_dt < 1e-6:
    #     return

    return dn_dt