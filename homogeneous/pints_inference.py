import numpy as np
import pints
import pints.plot
import pints_smol as toy
import matplotlib.pyplot as plt


model = toy.SmolModel(None,None)


true_parameters = [0.0004, 500]


times = np.linspace(0, 97, 97000)

org_values = model.simulate(true_parameters, times)

print(org_values)

print(org_values.shape)

noise = 25
values = org_values + np.random.normal(0, noise, org_values.shape)

size_noise = 100
noise_value = 25
# Create a list with the specified size filled with a placeholder value
noise_arr = [noise_value for _ in range(size_noise)]

problem = pints.MultiOutputProblem(model, times, values)

log_likelihood = pints.GaussianLogLikelihood(problem)

print('Original problem dimension: ' + str(problem.n_parameters()))
print('New dimension: ' + str(log_likelihood.n_parameters()))

true_parameters += noise_arr
print(true_parameters)


# Define the size of the list
size = 102
placeholder_lower_value = 1
placeholder_upper_value = 100
 
# Create a list with the specified size filled with a placeholder value
prior_arr_lower = [placeholder_lower_value for _ in range(size)]
prior_arr_upper = [placeholder_upper_value for _ in range(size)]
prior_arr_lower[0] = 0.00001
prior_arr_upper[0] = 0.01
prior_arr_lower[1] = 1
prior_arr_upper[1] = 1000

# log_prior = pints.UniformLogPrior(
#     [0.000001, 1, 1],
#     [0.01, 10000, 100]
#     )
log_prior = pints.UniformLogPrior(
    prior_arr_lower,
    prior_arr_upper
    )

# Create a posterior log-likelihood (log(likelihood * prior))
log_posterior = pints.LogPosterior(log_likelihood, log_prior)

xs = [
    np.array(true_parameters) * 0.9,
    np.array(true_parameters) * 1.05,
    np.array(true_parameters) * 1.15,
]

chains = pints.mcmc_sample(log_posterior, 3, xs)

print(chains)


pints.plot.trace(chains)
plt.show()