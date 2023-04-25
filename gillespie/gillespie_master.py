## Master code for implementing gillespie algorithm
import numpy as np

import initial_conditions
import step_functions as step_fns
import gillespie_plots as gill_plt

# Global constants
N = 100 # The maximal cluster size

# Initialisation
include_coagulation = True
include_mitosis = True
include_death = True
include_splitting = False

c_v = []
c_v = np.array(c_v)
c_cst = 0.01
m_cst = 0.01
d_cst = 0.01
s_cst = 0.001


if include_coagulation == True:
    for i in range(2500):
        c_v = np.append(c_v, c_cst)

if include_mitosis ==True:
    for i in range(2500,2599,1):
        c_v = np.append(c_v, m_cst)

if include_death ==True:
    for i in range(2599,2698,1):
        c_v = np.append(c_v, d_cst)

if include_splitting ==True:
    for i in range(2698,5198,1):
        c_v = np.append(c_v, s_cst)
print(c_v)
print('Length of c_v', len(c_v))
print(min(c_v))
print(c_v[0])


IC = initial_conditions.set_initial_conditions(N,3)
print(IC)
print(sum(IC))

t_init = 0
simulation_counter = 0
simulation_max = 100

psi_output = np.zeros((simulation_max + 1, N))
t_output = np.zeros(simulation_max + 1)

psi_output[0,:] = IC
psi_old = IC
t_old = t_init
t_output[0] = t_old
while simulation_counter < simulation_max:
    psi_new, t_new = step_fns.single_step(c_v, psi_old, t_old, N)
    simulation_counter += 1
    print('t is: ', t_new)
    t_output[simulation_counter] = t_new
    t_old = t_new
    psi_output[simulation_counter,:] = psi_new
    psi_old = psi_new
    print('New distribution', psi_new)

print('Output', psi_output)
print('Size', np.shape(psi_output))
print('T len', len(t_output))
gill_plt.animate_plot(psi_output, t_output)
