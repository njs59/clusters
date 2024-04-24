## Master code for implementing gillespie algorithm
import numpy as np
import math
import time

import initial_conditions
import step_functions as step_fns
import gillespie_plots as gill_plt
import constant_functions as cst_fns

###################
# Global constants
N = 100 # The maximal cluster size
M = 500 # The number of cells
sim_num = 1000 # The number of simulations
###################


# Initialisation
include_coagulation = True
include_shedding = True

include_mitosis = False
include_death = False
include_splitting = False


c_v = []
c_v = np.array(c_v)

# Set the proportions of the events that are 
# coagulations (b), mitosis (m), death (d), splitting (s)
lam = 1
b_prop = 1
s_prop = lam * b_prop
m_prop = 0
d_prop = 0

# Set values for c_v for each type of event
b_cst = cst_fns.coagulation_cst(b_prop, N)
print('b sum check', np.sum(b_cst))
print('S prob', s_prop)
s_cst = cst_fns.shed_cst(s_prop, N, 1) #3rd argument gives type of dependence (constant, linear, exponential, 2/3 power)
print('Shed cst', s_cst)

m_cst = m_prop/99
d_cst = cst_fns.death_cst(d_prop, N)


if include_coagulation == True:
    for i in range(2500):
        c_v = np.append(c_v, b_cst[i])

if include_shedding ==True:
    for i in range(2500,2599,1):
        c_v = np.append(c_v, s_cst[i-2500])

if include_mitosis ==True:
    for i in range(2599,2698,1):
        c_v = np.append(c_v, m_cst)

if include_death ==True:
    for i in range(2698,2797,1):
        c_v = np.append(c_v, d_cst[i - 2698])

# if include_splitting ==True:
#     for i in range(2698,5198,1):
#         c_v = np.append(c_v, s_cst)


print(c_v)
print('Length of c_v', len(c_v))
print(min(c_v))
print(c_v[0])

##############################
IC = initial_conditions.set_initial_conditions(N, 2, M)
print(IC)
print(sum(IC))

t_init = 0
# simulation_counter = 0
simulation_max = 30000
t_max = 96
############################

# psi_output = np.zeros((simulation_max + 1, N))
psi_output = IC
psi_output_kept = IC
t_output = np.zeros(simulation_max + 1)

# t_arr = [t_init]

start_time = time.time()

for i in range(sim_num):
    # IC = initial_conditions.set_initial_conditions(N,2,M)
    # psi_single_sim = np.zeros((simulation_max + 1, N))
    # psi_single_sim[0,:] = IC
    simulation_counter = 0
    t_arr = [t_init]
    psi_single_sim = IC
    psi_single_sim_old = IC
    psi_single_sim = IC
    t_old = t_init
    t_output[0] = t_old
    # while simulation_counter < simulation_max:
    while t_old < t_max:
        psi_single_sim = np.vstack([psi_single_sim,np.zeros((N))])
        psi_new, t_new = step_fns.single_step(c_v, psi_single_sim_old, t_old, N)
        IC = psi_single_sim[0,:]
        simulation_counter += 1
        if math.floor(simulation_counter/1000) == simulation_counter/1000:
            print('counter is: ', simulation_counter)
        t_output[simulation_counter] = t_new
        t_arr = np.append(t_arr, t_new)
        t_old = t_new
        psi_single_sim[simulation_counter,:] = psi_new
        psi_single_sim_old = psi_new
    
    # print(t_arr)
    index_required = []
    psi_out_kept = IC
    for p in range(1, t_max + 1):
        index_p = next(x for x, val in enumerate(t_arr) if val > p)
        index_required = np.append(index_required, index_p)
        psi_out_kept = np.vstack((psi_out_kept, psi_single_sim[index_p - 1,:]))

    if i == 0:
        psi_output_kept = psi_out_kept
    else:
        for j in range(N):
        #     # for k in range(simulation_counter + 1):
            for k in range(t_max + 1):
                psi_output_kept[k,j] += psi_out_kept[k,j]

    # if i == 0:
    #     psi_output = np.zeros((simulation_counter + 1, N))
    #     simulation_1_max = simulation_counter
    # else:
    #     if simulation_counter + 1 > psi_output.shape[0]:
    #         # Need to add zeros
    #         # Times could be different ???!!!
    #         # Somehow need to save times
    #         # Then plot at regular intervals
    #         print('AHH')
    #     else:
    #         # psi_output = np.vstack([psi_output,np.zeros(N,1)])
    #         print('Add here')
    # for j in range(N):
    #     # for k in range(simulation_counter + 1):
    #     for k in range(simulation_1_max + 1):
    #         psi_output[k,j] += psi_single_sim[k,j]
    print('Simulation', i, ' complete')
    simulation_counter = 0

psi_output = psi_output_kept
psi_output = psi_output/sim_num
end_time = time.time()

total_simulation_time = end_time - start_time
average_single_sim_time = total_simulation_time/sim_num

print('Output', psi_output)
print('Size', np.shape(psi_output))
print('T len', len(t_output))
print('Total simulation time', total_simulation_time)
print('Average single simulation time', average_single_sim_time)
start_time_plot = time.time()
# gill_plt.animate_plot(psi_output, t_output, simulation_max)
end_time_plot = time.time()
plotting_time = end_time_plot - start_time_plot
print('Plotting time', plotting_time)

np.savetxt("gill_out_time.csv", psi_output, delimiter=",", fmt='%f', header='')

# gill_plt.animate_plot_mass(psi_output, t_output, simulation_max)

gill_plt.final_step_plot(psi_output, t_output, simulation_max)

# gill_plt.final_step_normalise_plot(psi_output, t_output, simulation_max)

# gill_plt.final_step_mass_plot(psi_output, t_output, simulation_max)

# gill_plt.final_step_mass_hist(psi_output, t_output, simulation_max, sim_num)