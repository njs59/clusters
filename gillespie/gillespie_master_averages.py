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
M = 200
IC = initial_conditions.set_initial_conditions(N, 2, M)
print(IC)
print(sum(IC))

t_init = 0
simulation_counter = 0
simulation_max = 300
############################

psi_output = np.zeros((simulation_max + 1, N))
t_output = np.zeros(simulation_max + 1)

start_time = time.time()

for i in range(sim_num):
    IC = initial_conditions.set_initial_conditions(N,2,M)
    psi_single_sim = np.zeros((simulation_max + 1, N))
    psi_single_sim[0,:] = IC
    psi_single_sim_old = IC
    t_old = t_init
    t_output[0] = t_old
    while simulation_counter < simulation_max:
        psi_new, t_new = step_fns.single_step(c_v, psi_single_sim_old, t_old, N)
        simulation_counter += 1
        if math.floor(simulation_counter/1000) == simulation_counter/1000:
            print('counter is: ', simulation_counter)
        t_output[simulation_counter] = t_new
        t_old = t_new
        psi_single_sim[simulation_counter,:] = psi_new
        psi__single_sim_old = psi_new
    for j in range(N):
        for k in range(simulation_max + 1):
            psi_output[k,j] += psi_single_sim[k,j]
    print('Simulation', i, ' complete')
    simulation_counter = 0


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

# gill_plt.animate_plot_mass(psi_output, t_output, simulation_max)

gill_plt.final_step_plot(psi_output, t_output, simulation_max)

gill_plt.final_step_normalise_plot(psi_output, t_output, simulation_max)

gill_plt.final_step_mass_plot(psi_output, t_output, simulation_max)

gill_plt.final_step_mass_hist(psi_output, t_output, simulation_max, sim_num)