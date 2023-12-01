## Script to run multiple simulations of heterogeneous gillespie

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import initial_condition
import select_event
import event_update
import plots as gill_plt

initial_cells_number = 200
initial_pro_prop = 0.1
num_steps = 10000
print_every = 1000
num_sims = 100

init_array = initial_condition.initial_setup(initial_cells_number, initial_pro_prop)


data = ['Total cells', 'Proliferative cells', 'Timestep', 'Sim number']
curr_shape = init_array.shape
times = np.full((curr_shape[0], 1), 0)
curr_sim_number = np.full((curr_shape[0], 1), 1)
to_add = np.append(times, curr_sim_number, axis=1)
data_step = np.append(init_array, to_add, axis=1)

data = np.vstack((data, data_step))
for m in range(num_sims):
    for l in range(num_steps):
        event = select_event.event_selector(init_array)
        init_array = event_update.event_selector(init_array, event)

        curr_shape = init_array.shape
        times = np.full((curr_shape[0], 1), l+1)
        
        curr_sim_number = np.full((curr_shape[0], 1), m+1)
        to_add = np.append(times, curr_sim_number, axis=1)
        data_step = np.append(init_array, to_add, axis=1)

        if (l+1) % print_every == 0:                                                                   
            data = np.vstack((data, data_step))
        # print('Current array', array_test)

df = pd.DataFrame(data)

x = range(1,101)
y = data_step[:,0]
plt.hist(y,x)
plt.xlabel('Cluster size')
# plt.ylabel('Average number of clusters')
# plt.savefig("plots_to_gif/final_plot" + ".jpg")
plt.show()
plt.clf()

df.to_csv('data_multiple.csv', index=False, header=False)

import csv

with open('data2.csv', newline='') as csvfile:
    data_numerical = list(csv.reader(csvfile))

print(data_numerical)

# # gill_plt.animate_plot_mass(psi_output, t_output, simulation_max)

# gill_plt.final_step_plot(data, num_steps)

# gill_plt.final_step_normalise_plot(data, num_steps)

# gill_plt.final_step_mass_plot(data, num_steps)

# # gill_plt.final_step_mass_hist(psi_output, num_steps, sim_num)