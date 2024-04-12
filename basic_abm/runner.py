import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import functions as fns

x_len = 100
y_len = 100
next_available_ID = 1
initial_size = 40
initial_number = 5
timesteps = 10000

cols = ["ID", "Radius", "Centre x", "Centre y"]
cell_df = pd.DataFrame(columns=cols)



initial_df, next_available_ID = fns.initialise(initial_number,x_len,y_len,initial_size)

cell_df = fns.sweep(initial_df, x_len, y_len, next_available_ID)

visual_arr = fns.visualise_arr(cell_df, x_len, y_len)

print('Initial df', cell_df)

plt.imshow(visual_arr)
plt.show()


for i in range(timesteps):
    cell_df = fns.move_clusters(cell_df)

    cell_df = fns.sweep(cell_df, x_len, y_len, next_available_ID)

    visual_arr = fns.visualise_arr(cell_df, x_len, y_len)

    if i % 1000 == 0:
        print('Current df', cell_df)

        plt.imshow(visual_arr)
        plt.show()

print(initial_df)
