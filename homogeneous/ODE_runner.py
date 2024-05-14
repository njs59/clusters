import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as plt

import smol_ODE

N = 500

b_test = [0.0004, 0.0004, 0.0005, 0.0005]
# b_test = [0.0005]

m_test = [0, 0.1, 0, 0.1]
# m_test = [0.01]
# m = 0
# d = 0

## Running of solver
tmin = 0
tmax = 97
# tmax = 1000
tspan = np.linspace(tmin, tmax, 97000)

## IC 
# (set to allow for metastatic invasion)
# n0 = np.zeros((N,len(tspan)))
# n0[0,0] = 500
n0 = np.zeros((N))
n0[0] = 500

# for runs in range(0,len(b_test)):
# b = b_test[runs]
# run_number = runs
# [t,n] = ode45(@ext_smol, tspan, n0);

b = b_test[0]

result = odeint(smol_ODE.ext_smol,n0,tspan,args = (b,N))

final_time = result[-1,:]

N_t = 0
for i in range(len(final_time)):
    N_t += (i+1)*final_time[i]

print('Mass', N_t)

# plt.plot(result[-1,:],label='R0=0')
# # plt.plot(tspan,result[:,1],label='R0=1')
# plt.show()



noise = 0.1
values = result + np.random.normal(0, noise, result.shape)


plt.figure(figsize=(12,4.5))
plt.xlabel('Time')
plt.ylabel('Values')
plt.plot(values[-1,:], label='Noisy data')
plt.plot(result[-1,:], lw=2, label='Noise-free data')
plt.legend()
plt.show()

