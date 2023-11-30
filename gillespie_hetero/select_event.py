import math
import numpy as np
import random

import coagulation as coag
import shedding as shed

def event_selector(array):

    shape = array.shape
    # print('shape', shape)

    #Include coag kernel but for now just use diffusive kernel

    ## Sum chances of coagulation
    sum_coag = 0
    coag_cst = 1
    for i in range (shape[0]):
        # print(range(i,shape[0]))
        for j in range(i+1, shape[0]):
            # coag_cst = coag.coag_ker(0,i,j)
            sum_coag += coag_cst * (array[i,0] + array[j,0])/(array[i,0] * array[j,0])
    


    ## Sum chances of shedding
    sum_shed = 0
    shed_cst = 1
    for i in range(shape[0]):
        if array[i,1] > 1:
            sum_shed += shed_cst * (array[i,1])

    total_sum = sum_coag + sum_shed

    rand = random.random()
    # print('Random:', rand)
    # print('Prop coag', sum_coag/total_sum)

    if rand < sum_coag/total_sum:
        # Coag event occurs
        event_array = coag.coagulation_event(rand, sum_coag, array)


    else:
        # Shed event occurs
        event_array = shed.shedding_event(rand, shed_cst, sum_coag, sum_shed, array)

    # print('Event is', event_array)

    return event_array


