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

problem = pints.SingleOutputProblem(model, times, values)

log_likelihood = pints.GaussianLogLikelihood(problem)

print('Original problem dimension: ' + str(problem.n_parameters()))
print('New dimension: ' + str(log_likelihood.n_parameters()))

true_parameters += [noise]
print(true_parameters)

# log_prior = pints.UniformLogPrior(
#     [0.000001, 1],
#     [0.01, 100]
#     )

# # Create a posterior log-likelihood (log(likelihood * prior))
# log_posterior = pints.LogPosterior(log_likelihood, log_prior)

# xs = [
#     np.array(true_parameters) * 0.9,
#     np.array(true_parameters) * 1.05,
#     np.array(true_parameters) * 1.15,
# ]

# chains = pints.mcmc_sample(log_posterior, 3, xs)

# print(chains)


# pints.plot.trace(chains)
# plt.show()