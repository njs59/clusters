## Master code for implementing gillespie algorithm
import numpy as np
import math

import initial_conditions
import step_functions as step_fns
import gillespie_plots as gill_plt
import constant_functions as cst_fns

# Global constants
N = 100 # The maximal cluster size

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
lam = 0
b_prop = 1
s_prop = lam * b_prop
m_prop = 0
d_prop = 0

# Set values for c_v for each type of event
b_cst = cst_fns.coagulation_cst(b_prop, N)
print('b sum check', np.sum(b_cst))
s_cst = cst_fns.shed_cst(s_prop, N, 1) #3rd argument gives type of dependence (constant, linear, exponential)
print('Shed cst', s_cst)

m_cst = m_prop/99
d_cst = cst_fns.death_cst(d_prop, N)


if include_coagulation == True:
    for i in range(2500):
        c_v = np.append(c_v, b_cst[i])

if include_shedding ==True:
    for i in range(2500,2599,1):
        c_v = np.append(c_v, s_cst[i - 2500])
        # c_v = np.append(c_v, s_cst)

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


M = 500
IC = initial_conditions.set_initial_conditions(N,2,M)
print(IC)
print(sum(IC))

t_init = 0
simulation_counter = 0
simulation_max = 1000
t_max = 48

# psi_output = np.zeros((simulation_max + 1, 1))
t_output = np.zeros(simulation_max + 1)

# psi_output[0,:] = IC
psi_output = IC
psi_old = IC
t_old = t_init
t_output[0] = t_old
# while simulation_counter < simulation_max:
while t_old < t_max:
    psi_output = np.vstack([psi_output,IC])
    psi_new, t_new = step_fns.single_step(c_v, psi_old, t_old, N)
    simulation_counter += 1
    if math.floor(simulation_counter/1000) == simulation_counter/1000:
        print('counter is: ', simulation_counter)
    t_output[simulation_counter] = t_new
    t_old = t_new
    psi_output[simulation_counter,:] = psi_new
    psi_old = psi_new

print('Output', psi_output)
print('Size', np.shape(psi_output))
print('T len', len(t_output))
# gill_plt.animate_plot(psi_output, t_output, simulation_max)

gill_plt.final_step_plot(psi_output, t_output, simulation_max)
