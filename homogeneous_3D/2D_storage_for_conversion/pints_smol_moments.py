#
# Logistic toy model.
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import numpy as np
import pints
from scipy.integrate import odeint
from scipy.stats import moment

# from pints import ToyModel


class SmolModel(pints.ForwardModel):

    r"""
    Extends :class:`pints.ForwardModel`, :class:`pints.toy.ToyModel`.

    Parameters
    ----------
    initial_population_size : float
        Sets the initial population size :math:`p_0`.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Population_growth
    """

    def __init__(self, N, n0):
        super(SmolModel, self).__init__()

        # Check initial values
        if N is None:
            self._n0 = np.zeros((100))
            self._n0[0] = 500
        #     # self._y0 = np.array([38, 1, 0])
        else:
            self._n0 = np.array((100))
            self._n0[0] = N

    def n_outputs(self):
        """ See :meth:`pints.ForwardModel.n_outputs()`. """
        return 5

    def n_parameters(self):
        """ See :meth:`pints.ForwardModel.n_parameters()`. """
        # IN time change this to N + 1 parameters (one b for each size)
        return 2


    def cell_coagulation(self,n,i,b,t,N_t,N):

        ## Coagulation term calculation
        # scaling = (floor(N/2)+ceil(N/2))/(floor(N/2)*ceil(N/2)); %Scaling for diffusion kernel
        # scaling = floor(N/2)*ceil(N/2); %Scaling for multiplicative kernel
        scaling = 1
        if i > N_t:
            coagulation_sum = 0
        else:
            # 1st sum of coagulation term calculation
            sum1 = 0
            if i == 0:
                sum1 = 0

            elif i <= 100-1:
                for j in range(0,i):
                    sum1 += self.B_ij((i-j),j,b,scaling,t)*n[i-j-1]*n[j]

            if i == N_t:
                sum2 = 0
            else:
                # 2nd sum of coagulation term calculation
                sum2 = 0
                for j in range(0,min(100-i,N_t-i)):
                    sum2 += self.B_ij(i,j,b,scaling,t)*n[i]*n[j]
            
            coagulation_sum = (1/2)*sum1 - sum2


        coagulation = coagulation_sum
        return coagulation

    def B_ij(self,i,j,b,scaling,t):
        # Need very small b constant
        # WLOG b = 1
        # D_i = 1/i
        # D_j = 1/j
        # out = b*(1/scaling)*(D_i+D_j)
        # out = b*(1/scaling)*i*j
        out = b*1
        
        return out

        ## Functions
    def rhs_i(self,i,n,t,b,N):
        # b = b_test[run_number]

        # N_t = 0
        # N_t_before = 0

        # for l in range(0,100):
        #     N_t_before = (l+1)*n[l]+ N_t_before
        # N_t = round(N_t_before)
        N_t = 500



        coagulation = self.cell_coagulation(n,i,b,t,N_t,N)
        
        # lifespan = cell_proliferation(n,i,N,m);
        dni_dt = coagulation 

        return dni_dt


    def _rhs(self,n0,t_curr,b,N):
        N = int(N)
        dn_dt = np.zeros(100)
        for i in range(0,100):
            dn_dt[i] = self.rhs_i(i,n0,t_curr,b,N)

        return dn_dt



    def simulate(self, parameters, times):
        """ See :meth:`pints.ForwardModel.simulate()`. """
        b, N = parameters
        n0 = np.array(self._n0)
        n0[0] = N
        n = odeint(self._rhs, n0, times, (b,N))

        # 1st moment is mean, 1st centred moment should be array 6
        centred_moment_1 = moment(n, moment=1, axis=1)
        centred_moment_2 = moment(n, moment=2, axis=1)
        centred_moment_3 = moment(n, moment=3, axis=1)
        centred_moment_4 = moment(n, moment=4, axis=1)
        centred_moment_5 = moment(n, moment=5, axis=1)

        centred_moments = np.zeros((n.shape[0],5))
        centred_moments[:,0] = centred_moment_1
        centred_moments[:,1] = centred_moment_2
        centred_moments[:,2] = centred_moment_3
        centred_moments[:,3] = centred_moment_4
        centred_moments[:,4] = centred_moment_5

        return centred_moments

    def suggested_parameters(self):
        """ See :meth:`pints.toy.ToyModel.suggested_parameters()`. """

        return np.array([0.0004, 100])

    def suggested_times(self):
        """ See :meth:`pints.toy.ToyModel.suggested_times()`. """

        return np.linspace(0, 97, 97000)