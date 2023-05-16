import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma




# lambda_lower = 2
# lambda_upper = 2*math.log(lambda_lower) - math.log(2*lambda_lower - 1)

# psi_k = []
# for k in range(1,50,1):
#     psi_k.append(math.exp(-lambda_upper*k)*((gamma(k-1/2))/(gamma(1/2)*gamma(k+1)))*(((lambda_lower-1)**2/2*lambda_lower)+(3/2)*((1-(1/(2*lambda_lower)))/(k+1))))

# print(psi_k)

# plt.plot(psi_k)
# plt.show()


#########  Exact solutions to coagulation model with singleton input
t = []
psi_k = np.zeros((1000,100))
for i in range (0,1000,1):
    t.append(i*0.01)
    for k in range(1,101):
        t_current = i*0.01
        psi_k[i,k-1] = (t_current**(k-1))/((1+t_current)**(k+1))

for k in range(1,101):        
    plt.plot(t,psi_k[:,k-1])

plt.show()

for k in range(1,6):        
    plt.plot(t,psi_k[:,k-1])
    plt.legend(['k = 1', 'k = 2', 'k = 3', 'k = 4', 'k = 5'])

plt.show()

# for i in range(0,1000):        
#     plt.plot(psi_k[i,:])

# plt.show()
