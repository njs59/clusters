import numpy as np
import math
import cell_coagulation


## Functions
def rhs_i(i,n,t,b,m,N):
    # b = b_test[run_number]

    N_t = 0
    N_t_before = 0

    for l in range(0,N):
        N_t_before = (l+1)*n[l]+ N_t_before
    N_t = round(N_t_before)



    coagulation = cell_coagulation.cell_coagulation(n,i,b,t,N_t,N)
    
    lifespan = cell_proliferation(n,i,N,m)
    dni_dt = coagulation + lifespan 

    return dni_dt


def ext_smol(n0,t_curr,b,m,N):
    dn_dt = np.zeros(N)
    # n = n0
    sum_dn_dt = 0
    for i in range(0,N):
        dn_dt[i] = rhs_i(i,n0,t_curr,b,m,N)
    # if sum_dn_dt < 1e-6:
    #     return

    return dn_dt



def cell_proliferation(n,i,N,m):
    N_t = N
    scaling = 1
    if i == 0:
        proliferation = -m*2*math.sqrt(i+1)*n[i]
    elif i <= N-1:
        proliferation = m*2*math.sqrt(i)*n[i-1] - m*2*math.sqrt(i+1)*n[i]
    else:
        proliferation = m*2*math.sqrt(i)*n[i-1]

    return proliferation
