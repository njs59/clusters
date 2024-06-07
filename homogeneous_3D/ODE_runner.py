import numpy as np
import pandas as pd
from scipy.integrate import odeint
from numpy.linalg import norm

import matplotlib.pyplot as plt

import pints

import smol_ODE
import smol_ODE_Pro
import smol_ODE_Pro_SA

import scipy.io
# matlab_mat = scipy.io.loadmat('homogeneous/b_0.0005_m_0_n_arr.mat')
# matlab_mat = matlab_mat['n'] 

df = pd.read_csv('homogeneous/s11_inference_input_multi_well_t_20.csv', header=None)
org_values = np.transpose(df.to_numpy())
N = 100

# b_test = [0.0004, 0.0004, 0.0005, 0.0005]
# b_test = [0.05]
# b_test = [2.47e-04]
# b_test = [2.60e-04]
b_test = [2.49e-04]
# m_test = [0, 0.1, 0, 0.1]
# m_test = [0]
# m_test = [4.06e-03]
m_test = [2.08e-04]
# m = 0
# d = 0

## Running of solver
tmin = 1
tmax = 97
# tmax = 1000
tspan = np.linspace(tmin, tmax, 97)

## IC 
# (set to allow for metastatic invasion)
# n0 = np.zeros((N,len(tspan)))
# n0[0,0] = 500
n0 = np.zeros((N))
# n0[0] = 1500
# n0[0] = 1150
n0[0] = 1410

# for runs in range(0,len(b_test)):
# b = b_test[runs]
# run_number = runs
# [t,n] = ode45(@ext_smol, tspan, n0);

b = b_test[0]
m = m_test[0]

# result = odeint(smol_ODE.ext_smol,n0,tspan,args = (b,N))
# result = odeint(smol_ODE_Pro.ext_smol,n0,tspan,args = (b,m,N))
result = odeint(smol_ODE_Pro_SA.ext_smol,n0,tspan,args = (b,m,N))

final_time = result[-1,:]

N_t = 0
for i in range(len(final_time)):
    N_t += (i+1)*final_time[i]

print('Mass', N_t)

# plt.plot(result[-1,:],label='R0=0')
# # plt.plot(tspan,result[:,1],label='R0=1')
# plt.show()


# final_time_matlab = matlab_mat[-1,:]

# difference_final = norm(final_time-final_time_matlab)

# print('l2 norm', difference_final)

# noise = 0.1
# values = result + np.random.normal(0, noise, result.shape)

result_interested = result[19:,:]

result_grouped = np.zeros((78,20))
org_values_grouped = np.zeros((78,20))

for k in range(20):
    for l in range(5):
        result_grouped[:,k] += result_interested[:,k*5 + l]
        org_values_grouped[:,k] += org_values[:,k*5 + l]



for j in range(np.shape(org_values)[0]):
    plt.xlabel('Cluster Sizes')
    plt.ylabel('Values')
    plt.plot(result_interested[j,:], lw=2, label='Model outputs')
    plt.plot(org_values[j,:], label = 'Data outputs')
    plt.legend()
    plt.savefig(f'homogeneous/fit_plot_frames/SA_proliferation_frame-{j:02d}.png')
    plt.clf()

for j in range(np.shape(org_values_grouped)[0]):
    plt.xlabel('Cluster Sizes')
    plt.ylabel('Values')
    plt.plot(result_grouped[j,:], lw=2, label='Model outputs')
    plt.plot(org_values_grouped[j,:], label = 'Data outputs')
    plt.legend()
    plt.savefig(f'homogeneous/fit_plot_frames/grouped_cluster_sizes/SA_proliferation_frame-{j:02d}.png')
    plt.clf()
    # plt.show()



plt.figure(1,figsize=(12,4.5))
plt.xlabel('Cluster Sizes')
plt.ylabel('Values')
# plt.plot(values[-1,:], label='Noisy data')
plt.plot(result[-1,:], lw=2, label='Noise-free data')
plt.plot(org_values[-1,:])
plt.legend()
plt.show()

plt.figure(2,figsize=(12,4.5))
plt.xlabel('Cluster Sizes')
plt.ylabel('Values')
# plt.plot(values[-1,:], label='Noisy data')
plt.plot(result[19,:], lw=2, label='Noise-free data')
plt.plot(org_values[0,:])
plt.legend()
plt.show()



