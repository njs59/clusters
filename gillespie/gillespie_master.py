## Master code for implementing gillespie algorithm
import numpy as np

import initial_conditions
import step_functions as step_fns

# Global constants
N = 100 # The maximal cluster size

# Initialisation
include_coagulation = True
include_mitosis = False
include_death = False
include_splitting = False

c_v = []
c_v = np.array(c_v)
c_cst = 0.001
m_cst = 0.01
d_cst = 0.01
s_cst = 0.001

print(c_v)

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
print(len(c_v))
print(min(c_v))
print(c_v[0])


IC = initial_conditions.set_initial_conditions(N,1)
print(IC)
print(sum(IC))

t = 0
simulation_counter = 0
simulation_max = 1000

psi_output = np.zeros((simulation_max + 1, N))
t_output = np.zeros(simulation_max)

psi_output[0,:] = IC

while simulation_counter < simulation_max:
    psi_new = step_fns.single_step(c_v, psi_old, t, N)
    print('t is: ', t)
    psi_output[simulation_counter,:] = psi_new
    psi_old = psi_new
    simulation_counter += 1
