import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import functions as fns

x_len = 1000
y_len = 1000
next_available_ID = 1
initial_size = 200
initial_number = 500
timesteps = 50000

cols = ["ID", "Radius", "Centre x", "Centre y"]
cell_df = pd.DataFrame(columns=cols)



initial_df, next_available_ID = fns.initialise(initial_number,x_len,y_len,initial_size)

cell_df, next_available_ID = fns.sweep(initial_df, x_len, y_len, next_available_ID)

visual_arr = fns.visualise_arr(cell_df, x_len, y_len)

print('Initial df', cell_df)

# plt.imshow(visual_arr)
# plt.show()


for i in range(timesteps):
    cell_df = fns.move_clusters(cell_df, x_len, y_len)

    cell_df, next_available_ID = fns.sweep(cell_df, x_len, y_len, next_available_ID)

    # visual_arr = fns.visualise_arr(cell_df, x_len, y_len)
    if i % 100 == 0:
        print('Step', i , 'complete')

        if i % 1000 == 0:
            print('Current df', cell_df)

            visual_arr = fns.visualise_arr(cell_df, x_len, y_len)

            fig_num = int(i/100)

            plt.imshow(visual_arr)
            plt.savefig('/Users/Nathan/Documents/Oxford/DPhil/clusters/basic_abm/method2_figure_' + str(fig_num) + '_IC_500_steps_50000' + '.png')


print(initial_df)
