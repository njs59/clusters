#
# Logistic toy model.
#
# This file is part of PINTS (https://github.com/pints-team/pints/) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
import numpy as np
import pints
from numba import jit
from scipy.integrate import odeint

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
            print('Init 1')
        #     # self._y0 = np.array([38, 1, 0])
        else:
            self._n0 = np.array((100))
            self._n0[0] = N
            print('Init 2')

    def n_outputs(self):
        """ See :meth:`pints.ForwardModel.n_outputs()`. """
        return 100

    def n_parameters(self):
        """ See :meth:`pints.ForwardModel.n_parameters()`. """
        # IN time change this to N + 1 parameters (one b for each size)
        return 3


    def cell_coagulation(self,n,i,b,p,t,N_t,N):

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
                for j in range(0,min(100-i,N_t-i)-1):
                    sum2 += self.B_ij(i,j,b,scaling,t)*n[i]*n[j]
            
            coagulation_sum = (1/2)*sum1 - sum2


        coagulation = coagulation_sum
        return coagulation

    def B_ij(self,i,j,b,p,scaling,t):
        # Need very small b constant
        # WLOG b = 1
        # D_i = 1/i
        # D_j = 1/j
        # out = b*(1/scaling)*(D_i+D_j)
        # out = b*(1/scaling)*i*j
        out = b*1
        
        return out

        ## Functions
    @staticmethod
    def rhs_i(self,i,n,t,b,p,N):
        # b = b_test[run_number]

        # N_t = 0
        # N_t_before = 0

        # for l in range(0,100):
        #     N_t_before = (l+1)*n[l]+ N_t_before
        # N_t = round(N_t_before)
        N_t = 500



        coagulation = self.cell_coagulation(n,i,b,p,t,N_t,N)
        
        # lifespan = cell_proliferation(n,i,N,m);
        dni_dt = coagulation 

        return dni_dt

    @staticmethod
    @jit
    def _rhs(n0,t_curr,b,p,N):
        N = int(N)
        dn_dt = np.zeros(100)
        for i in range(0,100):
            # dn_dt[i] = SmolModel.rhs_i(i,n0,t_curr,b,N)
            N_t = N
            # coagulation = SmolModel.cell_coagulation(n0,i,b,t_curr,N_t,N)
            scaling = 1
            if i > N_t:
                coagulation_sum = 0
            else:
                # 1st sum of coagulation term calculation
                sum1 = 0
                if i == 0:
                    sum1 = 0
                    proliferation = -p*(i+1)*n0[i]

                elif i <= 100-1:
                    for j in range(0,i):
                        # sum1 += self.B_ij((i-j),j,b,scaling,t)*n[i-j-1]*n[j]
                        sum1 += b*1*n0[i-j-1]*n0[j]
                        proliferation = p*(i)*n0[i-1] - p*(i+1)*n0[i]


                if i == N_t:
                    sum2 = 0
                else:
                    # 2nd sum of coagulation term calculation
                    sum2 = 0
                    for j in range(0,min(100-i,N_t-i)-1):
                        sum2 += b*1*n0[i]*n0[j]
                    
                    proliferation = p*(i)*n0[i-1]
                
                coagulation_sum = (1/2)*sum1 - sum2


            coagulation = coagulation_sum
                # lifespan = cell_proliferation(n,i,N,m);
            dn_dt[i] = coagulation + proliferation


        return dn_dt



    def simulate(self, parameters, times):
        """ See :meth:`pints.ForwardModel.simulate()`. """
        b, p, N = parameters
        n0 = np.array(self._n0)
        n0[0] = N
        # n = odeint(self._rhs, n0, times, (b,N))
        # print('Times are:', times)
        # print('n0 is', n0)
        if times[0] != 0:
            time_gap = int(times[1] - times[0])
            previous_times = np.linspace(0, int(times[0]), int((int(times[0])-0)/time_gap) + 1)
            # print('Previous times', previous_times)
            # print('Inputs', n0, previous_times, b, N)
            n_previous_times = odeint(SmolModel._rhs, n0, previous_times, (b,p,N))
            n_input = n_previous_times[-1,:]
            # print('N input', n_input)
            # print('Length', len(n_input))
        else:
            n_input = n0
        n = odeint(SmolModel._rhs, n_input, times, (b,p,N))
        return n

    def suggested_parameters(self):
        """ See :meth:`pints.toy.ToyModel.suggested_parameters()`. """

        return np.array([0.0004, 0.001, 100])

    def suggested_times(self):
        """ See :meth:`pints.toy.ToyModel.suggested_times()`. """

        return np.linspace(0, 97, 97000)