import numpy as np
import random
import math
import logging

import update_psi

def single_step(c_v, psi, t, N):
    '''
    Performs a single step of the gillespie algorithm

    Inputs
    c_v: Vector of rates of equations
    psi: distribution of cluster size before the timestep
    t: Current time
    N: maximal cluster size
    '''
    eqns = len(c_v)

    r_0 = random.random()
    r_1 = random.random()
    h_v = calc_hv(eqns, psi)
    a_v = calc_av(eqns, h_v, c_v)
    a_0 = 0
    for i in range(eqns):
        a_0 += a_v[i]

    tau = (1/a_0)*np.log(1/r_0)

    comparison = r_1 * a_0
    mu = 0
    sum = 0
    for i in range(eqns):
        if sum < comparison:
            mu += 1
            sum += a_v[i]
        else:
            break

    # mu now corresponds to the subscript of the equation to be used to update psi
    # This corresponds to python indexing (i-1)
    t += tau
    python_mu = mu - 1
    psi_new = update_psi.update_master(psi, python_mu)
    ##RETURN
    return psi_new, t


########### Below this are functions for use in this file


def calc_hv(eqns, psi):
    '''
    Calculates the values for h_v s
    Only works for N = 100 (number of eqns change for maximal cluster size)
    '''
    index = 0
    h_v = np.zeros(eqns)
    for i in range(50):
        for j in range(i, 100-i-1):
            if j == i: # Clusters of same size have to be treated separately psi choose 2
                # As we have assumed i <= j it makes sense that we have a factor of 1/2 to not double 
                # count these interactions
                h_v[index] = (1/2) * psi[i] * psi[j]
                index += 1
            else:
                h_v[index] = psi[i] * psi[j]
                index += 1
    
    if eqns == 2500:
        return h_v
    

    else:
        for i in range(99):
            h_v[2500 + i] = psi[i]
        
        if eqns == 2599:
            return h_v
        
        else:
            for i in range(99):
                h_v[2599 + i] = psi[i+1]
            
            if eqns == 2698:
                return h_v
            
            else:
                index = 0
                for i in range(1,100):
                    for j in range(0, math.floor((i+1)/2)):
                        h_v[2698 + index] = psi[i]
                        index += 1
                
                if eqns == 5198:
                    return h_v
                else:
                    logging.error('Incorrect number of equations in h_v: ' + eqns)


def calc_av(eqns, h_v, c_v):
    if eqns != len(h_v):
        logging.error('Number of equations does not agree with length h_v: '+ eqns + len(h_v))
    elif eqns != len(c_v):
        logging.error('Number of equations does not agree with length c_v: '+ eqns + len(c_v))
    else:
        a_v = np.zeros(eqns)
        for i in range(eqns):
            a_v[i] = h_v[i] * c_v[i]
    return a_v

