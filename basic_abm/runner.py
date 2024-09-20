import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import functions as fns

x_len = 1025
y_len = 1344
next_available_ID = 1
initial_size = 200
initial_number = 500
timesteps = 5000

cols = ["ID", "Radius", "Centre x", "Centre y"]
cell_df = pd.DataFrame(columns=cols)

basedir = '/Users/Nathan/Documents/Oxford/DPhil/clusters/'


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
    if i % 10 == 0:
        print('Step', i , 'complete')

        if i % 10 == 0:
            print('Current df', cell_df)

            visual_arr = fns.visualise_arr(cell_df, x_len, y_len)

            fig_num = int(i/10)
            pd.DataFrame(visual_arr).to_csv(f'{basedir}basic_abm/csv_files_similar_exp/cell_500_every_10_im-frame-{i:01d}.csv', index=False, header=False)           

            pd.DataFrame(cell_df).to_csv(f'{basedir}basic_abm/csv_files_similar_exp/cell_500_every_10_im-df-{i:01d}.csv', index=False, header=True)           

            # plt.imshow(visual_arr)
            # plt.savefig('/Users/Nathan/Documents/Oxford/DPhil/clusters/basic_abm/method2_figure_' + str(fig_num) + '_IC_500_steps_50000' + '.png')


print(initial_df)
