import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import expon



def coagulation_cst(coag_proportion, N):
    prob_coag = np.zeros(2500)
    coag_cst = np.zeros(2500)
    for index in range(2500):
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
        
        ## Diffusion based kernel
        # D_i = 1/i
        # D_j = 1/j
        # prob_coag[index] = (D_i +D_j)

        ## Constant kernel
        # prob_coag[index] = 1

        ## Multiplicative kernel
        prob_coag[index] = i*j
    
    sum_prob_coag = np.sum(prob_coag)
    coag_cst = coag_proportion * (prob_coag/sum_prob_coag)

    # plt.plot(coag_cst)
    # plt.show()
    print('Sum', np.sum(coag_cst))

    return coag_cst


#
def shed_cst(shed_proportion, N, shed_type):
    shed_prop = np.zeros(99)
    shed_prob = np.zeros(99)
    shed_cst = np.zeros(99)
    if shed_type == 1: #Constant dependence
        for i in range(99):
            shed_prob[i] = 1/99
    if shed_type == 2: #Linear dependence
        for i in range(99):
            shed_prop[i] = i+1
        shed_sum = np.sum(shed_prop)
        for j in range(99):
            shed_prob[j] = shed_prop[j]/shed_sum
    if shed_type == 3: #Exponential dependence
        for i in range(99):
            shed_prop[i] = math.exp((i+1)/20)
        shed_sum = np.sum(shed_prop)
        for j in range(99):
            shed_prob[j] = shed_prop[j]/shed_sum
    if shed_type == 4: #Power 2/3
        for i in range(99):
            shed_prop[i] = i**(2)
        shed_sum = np.sum(shed_prop)
        for j in range(99):
            shed_prob[j] = shed_prop[j]/shed_sum

    shed_cst = shed_proportion*shed_prob

    return shed_cst




#calculate probability that x is less than 50 when mean rate is 40
def death_cst(death_proportion, N):
    prob_an = np.zeros(N)
    prob_ap = np.zeros(N)
    prob_tot = np.zeros(N)
    death_cst = np.zeros(N)
    for i in range(1, N+1):
        prob_an[i-1] = expon.cdf(x=i, scale=40) - expon.cdf(x=i-1, scale=40)
        prob_ap[i-1] = expon.cdf(x= N - i + 1, scale=40) - expon.cdf(x= N - i + 1 - 1, scale=40)
        prob_tot[i-1] = prob_an[i-1] + prob_ap[i-1]
        sum = np.sum(prob_tot)

    for j in range(1, N+1):
        death_cst[j-1] = 0*(prob_tot[j-1]*death_proportion) * (1/sum)
    # Plot current death constant
    # plt.plot(death_cst)
    # plt.show()
    print('Sum death', np.sum(death_cst))
    return death_cst