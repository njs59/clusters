import math

def update_master(psi, index):
    '''
    Function to update psi with new distribution once equation of iven index is applied

    Input:
    psi: distribution of cluster sizes to be updated
    index: Integer between 0 and 5197 for python subscript of corresponding equation

    Ouput:
    psi: UPdated distribution of cluster sizes
    '''
    if index in range(0, 2500):
        ## Coagulation update
        index_maths = index + 1
        i = 1
        ticker = 99
        while ticker < index_maths:
            i += 1
            ticker += (101- 2*i)
        else:
            last_lower_i = i
            last_lower = ticker - (101 - 2*i)
            diff = index - last_lower
            j = diff + last_lower_i
            # print('Value check', last_lower_i, last_lower, diff, j)
        ## (i,j) now corresponds to the size of the 2 clusters to coagulate
        ij_cluster = i + j
        i_python = i-1
        j_python = j-1
        ij_python = ij_cluster - 1
        # print('python sizes', i_python, j_python)
        if psi[i_python] <= 0 or psi[j_python] <= 0:
            print('Attempted to coagulate a cluster that does not exist')
        elif psi[i_python] == 1 and psi[j_python] == 1 and i_python == j_python:
            psi = psi # Keep psi the same as we don't coagulate a cluster with itself
            # print('Attempted to coagulate a cluster with itself')
        else:
            psi[i_python] -= 1 # Remove 1 cluster of size i
            psi[j_python] -= 1 # Remove 1 cluster of size j
            psi[ij_python] += 1 # Add 1 cluster of size i+j

    elif index in range(2500, 2599):
        ## Shedding code
        if psi[index - 2500 + 1] <=0:
            print('Attempted to shed a cluster that does not exist')
        else:
            psi[index - 2500 + 1] -= 1 # Remove 1 cluster of size i
            psi[index - 2500] += 1 # Add 1 cluster of size i-1
            psi[0] += 1 # Add 1 cluster of size 1

    elif index in range(2599, 2598):
        ## Mitosis update
        psi[index - 2599] -= 1 # Remove 1 cluster of size i
        psi[index - 2599 + 1] += 1 # Add 1 cluster of size i+1
    elif index in range(2698, 2797):
        ## Death update
        psi[index - 2698 + 1] -= 1 # Remove 1 cluster of size i
        psi[index - 2698] += 1 # Add 1 cluster of size i-1
    

    ## Code for splitting fragmentation
    # elif index in range(2698, 5198):
    #     ## Splitting update
    #     index_maths = index - 2698 + 1
    #     i = 2
    #     ticker = 1
    #     while ticker < index_maths:
    #         i += 1
    #         ticker += math.floor(i/2)
    #     else:
    #         last_lower_i = i-1
    #         last_lower = ticker - math.floor(i/2)
    #         diff = index - 2698 + 1 - last_lower
    #         j = diff
    #     ## (i,j) now corresponds to cluster of size i splitting into clusters
    #     # of sizes j & i-j where j <= i-j
    #     i_python = i-1
    #     j_python = j
    #     psi[i_python] -= 1 # Remove 1 cluster of size i
    #     psi[j_python] += 1 # Remove 1 cluster of size j
    #     psi[i_python - j_python] += 1 # Add 1 cluster of size i-j

    return psi
        