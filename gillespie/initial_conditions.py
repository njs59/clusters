import matplotlib.pyplot as plt
from scipy.stats import expon
import matplotlib.pyplot as plt
import numpy as np


def set_initial_conditions(N, opt, M):
    '''
    Returns the initial conditions psi_i for gillespie algorithm

    Inputs

    N: maximal cluster size

    opt: option for I.C.
        for opt = 1 we have constant I.C.
        for opt = 2 we have only clusters of size 1
        for opt = 3 we have exponential distribution of cluster sizes

    M: for opt 2 M is number of inputted singletons
    
    Returns:

    IC: The initial condition
    '''
    # May add in PSI: total number of initial clusters
    # but that needs conditions
    IC = np.zeros(N)

    if opt == 1:
        IC = np.ones(N)
    
    if opt == 2:
        IC[0] = M

    if opt == 3:
        # fig, ax = plt.subplots(1, 1)
        ax = plt.gca() # get axis handle

        r = expon.rvs(size=100)

        x = np.linspace(expon.ppf(0.01),
                expon.ppf(0.99), 100)

        n, bins, patches = plt.hist(r, bins=100, histtype='stepfilled', alpha=0.2)
        plt.show()

        heights = n
        print(heights)
        IC = heights

    return IC

