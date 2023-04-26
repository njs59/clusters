import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

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
        death_cst[j-1] = (prob_tot[j-1]*death_proportion) * (1/sum)
    # Plot current death constant
    plt.plot(death_cst)
    plt.show()
    print('Sum', np.sum(death_cst))
    return death_cst

