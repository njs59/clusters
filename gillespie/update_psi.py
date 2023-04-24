import numpy as np
import math

def update_master(psi, index):
    '''
    Function to update psi with new distribution once equation of iven index is applied

    Input:
    psi: distribution to be updated
    index: Integer between 0 and 5197 for python subscript of corresponding equation
    '''
    if index in range(0, 2500):
        ## Coagulation update
        index_maths = index + 1
        i = 1
        ticker = 99
        if ticker < index_maths:
            i += 1
            ticker += (101- 2*i)
        else:
            last_lower_i = i-1
            last_lower = ticker - (101 - 2*i)
            diff = index - last_lower
            j = diff + last_lower_i
        ## (i,j) now corresponds to the size of the 2 clusters to coagulate
        i_python = i-1
        j_python = j-1
        psi[i_python] -= 1 # Remove 1 cluster of size i
        psi[j_python] -= 1 # Remove 1 cluster of size j
        psi[i_python + j_python] += 1 # Add 1 cluster of size i+j

    elif index in range(2500, 2599):
        ## Mitosis update
        psi[index - 2500] -= 1 # Remove 1 cluster of size i
        psi[index - 2500 + 1] += 1 # Add 1 cluster of size i+1
    elif index in range(2599, 2698):
        ## Death update
        psi[index - 2500 + 1] -= 1 # Remove 1 cluster of size i
        psi[index - 2500] += 1 # Add 1 cluster of size i-1
    elif index in range(2698, 5198):
        ## Splitting update
        index_maths = index - 2698 + 1
        i = 2
        ticker = 1
        if ticker < index_maths:
            i += 1
            ticker += math.floor(i/2)
        else:
            last_lower_i = i-1
            last_lower = ticker - math.floor(i/2)
            diff = index - last_lower
            j = diff + last_lower_i
        ## (i,j) now corresponds to cluster of size i splitting into clusters
        # of sizes j & i-j where j <= i-j
        i_python = i-1
        j_python = j-1
        psi[i_python] -= 1 # Remove 1 cluster of size i
        psi[j_python] += 1 # Remove 1 cluster of size j
        psi[i_python - j_python] += 1 # Add 1 cluster of size i+j
        