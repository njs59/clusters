import pints
import numpy as np

import matplotlib.pyplot as plt

import smol_ODE



model = smol_ODE.ext_smol()

N = 500
n0 = np.zeros((N))
n0[0] = 500


times = np.linspace(0, 97, 97000)

true_parameters = [n0, times, 0.0004, N]

org_values = model.simulate(true_parameters, times)

noise = 0
values = org_values + np.random.normal(0, noise, org_values.shape)


plt.figure(figsize=(12,4.5))
plt.xlabel('Time')
plt.ylabel('Values')
plt.plot(times, values, label='Noisy data')
plt.plot(times, org_values, lw=2, label='Noise-free data')
plt.legend()
plt.show()


problem = pints.SingleOutputProblem(model, times, values)


log_likelihood = pints.GaussianLogLikelihood(problem)