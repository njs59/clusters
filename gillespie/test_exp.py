import matplotlib.pyplot as plt
from scipy.stats import expon
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1)

r = expon.rvs(size=1000000)

x = np.linspace(expon.ppf(0.01),
                expon.ppf(0.99), 100)

ax.hist(r, density=True, bins=100, histtype='stepfilled', alpha=0.2)
ax.set_xlim([x[0], x[-1]])
ax.legend(loc='best', frameon=False)
plt.show()