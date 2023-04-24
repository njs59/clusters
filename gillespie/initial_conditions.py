import matplotlib.pyplot as plt
from scipy.stats import expon
import matplotlib.pyplot as plt
import numpy as np


def set_initial_conditions(N, opt):
    '''
    Returns the initial conditions psi_i for gillespie algorithm

    Inputs

    N: maximal cluster size

    opt: option for I.C.
        for opt = 1 we have constant I.C.
        for opt = 2 we have only clusters of size 1
        for opt = 3 we have exponential distribution of cluster sizes
    
    Returns:

    IC: The initial condition
    '''
    # May add in PSI: total number of initial clusters
    # but that needs conditions
    IC = np.zeros(N)

    if opt == 1:
        IC = np.ones(N)
    
    if opt == 2:
        IC[0] = 100

    if opt == 3:
        fig, ax = plt.subplots(1, 1)

        r = expon.rvs(size=1000)

        x = np.linspace(expon.ppf(0.01),
                expon.ppf(0.99), 100)

        ax.hist(r, density=True, bins=100, histtype='stepfilled', alpha=0.2)
        ax.set_xlim([x[0], x[-1]])
        ax.legend(loc='best', frameon=False)
        plt.show()


        # x = np.random.rand(100)
        plt.hist(r)
        # plt.show()
        ax2 = plt.gca() # get axis handle

        p = ax2.patches
        p[0].get_height()

        heights = [patch.get_height() for patch in p]
        print(heights)
        IC = heights

    return IC

