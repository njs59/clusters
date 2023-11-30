import numpy as np
import pandas as pd

import initial_condition
import select_event
import event_update



initial_cells_number = 200
initial_pro_prop = 0.1

init_array = initial_condition.initial_setup(initial_cells_number, initial_pro_prop)



data = ['Total cells', 'Proliferative cells', 'Timestep']
curr_shape = init_array.shape
times = np.full((curr_shape[0], 1), 0)
data_step = np.append(init_array, times, axis=1)

data = np.vstack((data, data_step))

for l in range(1000):
    event = select_event.event_selector(array_test)
    array_test = event_update.event_selector(array_test, event)

    curr_shape = array_test.shape
    times = np.full((curr_shape[0], 1), l+1)
    data_step = np.append(array_test, times, axis=1)
                                                                        
    data = np.vstack((data, data_step))
    # print('Current array', array_test)

df = pd.DataFrame(data)
df.to_csv('data2.csv', index=False, header=False)