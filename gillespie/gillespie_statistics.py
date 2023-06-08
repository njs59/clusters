import numpy as np
import matplotlib.pyplot as plt
import math

def final_step_plot(psi, t, simulation_max, M):
    n_max = np.max(psi)
    # plots_number = simulation_max
    x = range(1,101)
    for i in range(simulation_max):
        y = psi[i,:]
        y_sum = 0
        for j in range(100):
            y_sum += y[j]


    plt.bar(x,y)
    plt.xlabel('Cluster size')
    plt.ylabel('Average number of clusters')
    plt.savefig("plots_to_gif/final_plot" + ".jpg")
    plt.clf()