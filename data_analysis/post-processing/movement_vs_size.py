# Compare movement distance against size of cluster
# Look for patterns
# Think it's Brownian motion
# Need to considerr how coagulation event effects supposed movement (centre jumps)


# Write code to watch each coagulation events
# Go a few frames before and after each coagulation event and watch
# just the clusters involved in the event
import math
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import lineage_tracer_function as ltf

start_time = 35
end_time = 97
basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_type = 'In_vitro_homogeneous_data/'
experiment = 'RAW_data/2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03'

well_loc = 's12'

timejump = 10

movement_values = []


for i in range(start_time, end_time+1, timejump):
    print('i is: ', i)

    df_start_csv_name_list = basedir, exp_type, 'post_processing_output/' , exp_date, '/', well_loc, 't', str(i-timejump).zfill(2) , 'c2_post_processing', '.csv'
    df_start_csv_name_list_2  =''.join(df_start_csv_name_list)
    df_start = pd.read_csv(df_start_csv_name_list_2)

    cluster_start_tags = df_start["Tag number"].to_numpy().astype(int)


    df_end_csv_name_list = basedir, exp_type, 'post_processing_output/' , exp_date, '/', well_loc, 't', str(i).zfill(2) , 'c2_post_processing', '.csv'
    df_end_csv_name_list_2  =''.join(df_end_csv_name_list)
    df_end = pd.read_csv(df_end_csv_name_list_2)

    cluster_end_tags = df_end["Tag number"].to_numpy().astype(int)


    # Include list of indexes around coagulations to ignore


    for j in range(len(cluster_end_tags)):
        tag_of_interest = cluster_end_tags[j]

        if tag_of_interest in cluster_start_tags:


            new_row_of_interest = df_end.loc[df_end['Tag number'] == tag_of_interest]
            new_size = new_row_of_interest['Cluster size'].values[0]
            new_x = new_row_of_interest['Cluster Centre x'].values[0]
            new_y = new_row_of_interest['Cluster Centre y'].values[0]

            old_row_of_interest = df_start.loc[df_start['Tag number'] == tag_of_interest]
            old_size = old_row_of_interest['Cluster size'].values[0]
            old_x = old_row_of_interest['Cluster Centre x'].values[0]
            old_y = old_row_of_interest['Cluster Centre y'].values[0]

            difference_percent = 100*abs(new_size - old_size)/old_size

            if difference_percent > 20:
                continue

            average_size = (new_size + old_size)/2
            movement = abs(new_x - old_x) + abs(new_y - old_y)


            vals_to_add = np.array([average_size, movement])

            movement_values = np.append(movement_values, vals_to_add)





movement_array = np.reshape(movement_values, (-1, 2))

# z = np.polyfit(movement_array[:,0], movement_array[:,1], 1)
# p = np.poly1d(z)

plt.scatter(movement_array[:,0], movement_array[:,1])
# plt.plot(movement_array[:,0], p(movement_array[:,0]), color='r', linestyle='--', label='fit')
plt.show()

