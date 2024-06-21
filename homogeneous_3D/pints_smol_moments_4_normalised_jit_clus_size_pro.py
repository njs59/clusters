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
from scipy.stats import moment

import math

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
            # print('Init 1')
        #     # self._y0 = np.array([38, 1, 0])
        else:
            self._n0 = np.array((100))
            self._n0[0] = N
            # print('Init 2')

    def n_outputs(self):
        """ See :meth:`pints.ForwardModel.n_outputs()`. """
        return 4

    def n_parameters(self):
        """ See :meth:`pints.ForwardModel.n_parameters()`. """
        # IN time change this to N + 1 parameters (one b for each size)
        return 3


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


        # 1st moment is mean, 1st centred moment should be array 6
        centred_moment_1 = moment(n, moment=1, axis=1)
        centred_moment_2 = moment(n, moment=2, axis=1)
        centred_moment_3 = moment(n, moment=3, axis=1)
        centred_moment_4 = moment(n, moment=4, axis=1)

        # Out array, mean, variance then centred standardised moments (aka skewness, kurtosis, hyperskewness)
        st_dev = np.sqrt(centred_moment_2)
        out_array = np.zeros((n.shape[0],4))
        out_array[:,0] = np.mean(n,axis=1)
        out_array[:,1] = centred_moment_2
        out_array[:,2] = np.divide(centred_moment_3,st_dev*st_dev*st_dev)
        out_array[:,3] = np.divide(centred_moment_4,st_dev*st_dev*st_dev*st_dev)

        # Standardized
        # st_dev = np.sqrt(centred_moment_2)
        # centred_moments = np.zeros((n.shape[0],5))
        # centred_moments[:,0] = np.divide(centred_moment_1,st_dev)
        # centred_moments[:,1] = np.divide(centred_moment_2,st_dev*st_dev)
        # centred_moments[:,2] = np.divide(centred_moment_3,st_dev*st_dev*st_dev)
        # centred_moments[:,3] = np.divide(centred_moment_4,st_dev*st_dev*st_dev*st_dev)
        # centred_moments[:,4] = np.divide(centred_moment_5,st_dev*st_dev*st_dev*st_dev*st_dev)

        return out_array
        # return n

    def suggested_parameters(self):
        """ See :meth:`pints.toy.ToyModel.suggested_parameters()`. """

        return np.array([0.0004, 0.01, 100])

    def suggested_times(self):
        """ See :meth:`pints.toy.ToyModel.suggested_times()`. """

        return np.linspace(0, 97, 97000)