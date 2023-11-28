import numpy as np
import pandas as pd

import select_event
import event_update


import os
# Make sure we are in the correct working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

## SIngleton only initial condition

# initial_cells_number = 200
# inital_pro_prop = 0.5

# array = np.full((initial_cells_number, 2), 1, dtype=int)

# initial_pro = int(inital_pro_prop * initial_cells_number)
# print(initial_pro)
# for i in range(initial_pro):
#     array[i,-1] = 0

# print(array)
# print(array.shape)
# print(array.shape[0])

initial_cells_number = 200
inital_pro_prop = 0.1

array_test = np.full((initial_cells_number, 2), 1, dtype=int)

initial_pro = int(inital_pro_prop * initial_cells_number)
print(initial_pro)
for i in range(initial_pro):
    array_test[i,-1] = 0

data = ['Total cells', 'Proliferative cells', 'Timestep']
curr_shape = array_test.shape
times = np.full((curr_shape[0], 1), 0)
data_step = np.append(array_test, times, axis=1)

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

