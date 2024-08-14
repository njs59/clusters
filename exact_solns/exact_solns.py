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
N_TOT = 500
psi_k = np.zeros((1000,100))
for i in range (0,1000,1):
    t.append(i*0.01)
    for k in range(1,101):
        t_current = i*0.01
        psi_k[i,k-1] = N_TOT*(t_current**(k-1))/((1+t_current)**(k+1))

for k in range(1,101):        
    plt.plot(t,psi_k[:,k-1])

plt.show()

for k in range(1,6):        
    plt.plot(t,psi_k[:,k-1])
    plt.legend(['k = 1', 'k = 2', 'k = 3', 'k = 4', 'k = 5'])

plt.show()

print(psi_k[-1,:])

num_clus = []
av_clus = []
for l in range(1000):
    num_clus = np.append(num_clus,np.sum(psi_k[l,:]))
    sum_clus = 0
    for m in range(100):
        sum_clus += (m+1)*psi_k[l,m]
    aver_clus = sum_clus/np.sum(psi_k[l,:])

    av_clus = np.append(av_clus, aver_clus)

plt.plot(num_clus)
plt.savefig('/Users/Nathan/Documents/Oxford/DPhil/clusters/exact_solns/num_clus.png')
plt.show()

plt.plot(av_clus)
plt.savefig('/Users/Nathan/Documents/Oxford/DPhil/clusters/exact_solns/average_clus_size.png')
plt.show()


# for m in range(10):
    # plt.hist(psi_k[100*m,:], bins=20)
plt.hist(psi_k[100,:])

plt.show()

# for i in range(0,1000):        
#     plt.plot(psi_k[i,:])

# plt.show()
