import math
import numpy as np
import random

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
        i_curr = 0
        j_curr = 1
        chances = (coag_cst * (array[i_curr,0] + array[j_curr,0])/(array[i_curr,0] * array[j_curr,0]))/sum_coag
        while chances < rand:
            if j_curr == shape[0] - 1:
                i_curr += 1
                j_curr = i_curr + 1
            else:
                j_curr += 1
            chances += (coag_cst * (array[i_curr,0] + array[j_curr,0])/(array[i_curr,0] * array[j_curr,0]))/sum_coag

        event_array = [i_curr, j_curr]

    else:
        # Shed event occurs
        k_curr = 0
        chances_shed = (shed_cst * (array[k_curr,1]))/sum_shed
        shed_found = False

        while shed_found == False:
            if k_curr == shape[0]:
                print('Attempted impossible shedding')
                event_array = []
                shed_found = True
            elif array[k_curr,1] <= 1:
                k_curr += 1
            else:
                chances_shed += (shed_cst * (array[k_curr,1]))/sum_shed
                if (sum_coag/total_sum) + chances_shed > rand:
                    shed_found = True
                else:
                    k_curr += 1
        
        event_array = [k_curr]

    # print('Event is', event_array)

    return event_array


