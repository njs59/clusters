import math
import numpy as np
import random

def event_selector(array, event_selection):
    
    if len(event_selection) == 2:
        # Coag event
        index_1 = event_selection[0]
        index_2 = event_selection[1]
        array[index_1,:] = array[index_1,:] + array[index_2,:]
        
        array_new = np.delete(array, index_2, 0)


    elif len(event_selection) == 1:
        # Shed event
        index = event_selection[0]
        array[index,:] = array[index,:] - 1
        array_new = np.append(array, [[1,1]], axis=0) 

        # array_new = array
    
    elif len(event_selection) == 0:
        # Failed Shed event
        array_new = array

    return array_new