import csv
import numpy as np
import pandas as pd
import time

import matplotlib.pyplot as plt

from scipy.ndimage import *

import post_pro_operators as post_oper

t_before = time.time()


basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_date = '2017-02-03'
time_array = range(1,98)
# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(2) for x in time_array]
well_loc = 's11'

cols = ["Tag number", "Cluster size", "Cluster Centre x", "Cluster Centre y", 
           "Event", "Clusters in event", "Timestep", "Date", "Well ID"]


next_available_tag = 1
for i in range(len(time_list)):

    t_before_step = time.time()

    csv_name_list = basedir, 'csv_folder/', exp_date, '_sphere_timelapse_', well_loc, 't', time_list[i], 'c2_area', '.csv'
    csv_name_list_2  =''.join(csv_name_list)

    df_area = pd.read_csv(csv_name_list_2, header=None)

    array_area_current_time = df_area.to_numpy()

    csv_name_list_index = basedir, 'csv_folder/', exp_date, '_sphere_timelapse_', well_loc, 't', time_list[i], 'c2_indexed', '.csv'
    csv_name_list_2_index  =''.join(csv_name_list_index)

    df_index = pd.read_csv(csv_name_list_2_index, header=None)

    array_index_current_time = df_index.to_numpy()
    
    # ##### Re-binarize array
    # slice_binary = (array_area_current_time > 0).astype(np.int_)

    # label_arr, num_clus = label(slice_binary)

    df_step = pd.DataFrame(np.nan, index=range(array_index_current_time.max()), columns=cols)
    df_step["Event"] = ""
    df_step["Clusters in event"] = ""

    centres_2D_current = post_oper.calc_clus_centre(array_index_current_time)


    area_2D_current = []
    for j in range(1,array_index_current_time.max()+1):
        loc_x = np.where(array_index_current_time==j)[0][0]
        loc_y = np.where(array_index_current_time==j)[1][0]
        area_2D_current.append(array_area_current_time[loc_x,loc_y])

    if i == 0:
        tag_number_current = []
        for k in range(1,array_index_current_time.max()+1):
            loc_x = np.where(array_index_current_time==k)[0][0]
            loc_y = np.where(array_index_current_time==k)[1][0]
            # Create list of tagged indices
            tag_number_current.append(array_index_current_time[loc_x,loc_y])

        centres_2D_old = centres_2D_current
        next_available_tag = array_index_current_time.max()+1

    else:
        tag_number_current = []
        for k in range(1,array_index_current_time.max()+1):
            same_locs, same_locs_store = post_oper.previous_clusters_at_loc(array_index_current_time, centres_2D_old, k)

            if same_locs == 1:
                #Simple, it's just movement
                # print('Move')
                mask = (df_old['Cluster Centre x'] == same_locs_store[0]) & (df_old['Cluster Centre y'] == same_locs_store[1])
                matching_row = df_old[mask]

                cluster_tag_number = matching_row['Tag number'].tolist()[0]
                tag_number_current.append(cluster_tag_number)
                # print('Yay 2')

                df_step.iloc[k-1,4] = 'Move'
                # df_step.iloc[k-1,5] = str([0])

            elif same_locs == 0:
                # Splitting
                # print('Split')
                tag_number_current.append(next_available_tag)
                next_available_tag += 1
                search_radius = 50

                x_cen = int(centres_2D_current[k-1][0])
                y_cen = int(centres_2D_current[k-1][1])

                # Compares with previous timestep array
                near_clus, clus_distances = post_oper.nearby_clusters(x_cen, y_cen, search_radius, array_index_old)

                if len(near_clus) == 0:
                    print('No nearby clusters')
                    df_step.iloc[k-1,4] = 'Appearance'
                    # df_step.iloc[k-1,5] = str([0])

                else:
                    cluster_index_split_from = post_oper.pick_cluster_inverse_dist(near_clus, clus_distances)
                    cluster_ID = df_old.iloc[cluster_index_split_from - 1 , 0]
                    old_cluster_size = df_old.iloc[cluster_index_split_from - 1 , 1]
                    new_cluster_size = area_2D_current[k-1]
                    percent_diff = 100*(abs(new_cluster_size - old_cluster_size))/((old_cluster_size+new_cluster_size)/2)
                    if percent_diff < 20:
                        df_step.iloc[k-1,0] = cluster_ID
                        df_step.iloc[k-1,4] = 'Move large'
                        df_step.iloc[k-1,5] = str([cluster_ID])
                    else:
                        df_step.iloc[k-1,4] = 'Splitting'
                        df_step.iloc[k-1,5] = str([cluster_ID])
                # print('Yay 3')


            else:
                # same_locs will be greater than 1 so we have coagulation
                # print('Coag')
                rows_to_save = []
                for s in range(same_locs):
                    mask = (df_old['Cluster Centre x'] == same_locs_store[s,0]) & (df_old['Cluster Centre y'] == same_locs_store[s,1])
                    rows_to_save.append(np.where(mask == True)[0][0])
                clusters_coagulating = df_old.iloc[rows_to_save]

                cluster_tag_number = min(clusters_coagulating['Tag number'])
                clusters_in_event = clusters_coagulating['Tag number'].tolist()

                df_step.iloc[k-1,4] = 'Coagulation'
                df_step.iloc[k-1,5] = str(clusters_in_event)

                tag_number_current.append(cluster_tag_number)
        

        # Update centres_2D_old for use in next timestep
        centres_2D_old = centres_2D_current
        




    print(centres_2D_current.shape)
    # print(area_2D_current)

    df_step.iloc[:,0] = tag_number_current
    df_step.iloc[:,1] = area_2D_current
    df_step.iloc[:,2] = centres_2D_current[:,0].tolist()
    df_step.iloc[:,3] = centres_2D_current[:,1].tolist()
    df_step.iloc[:,6] = time_list[i]
    df_step.iloc[:,7] = exp_date
    df_step.iloc[:,8] = well_loc

    # print(df_step)

    df_old = df_step
    array_index_old = array_index_current_time

    print('Yay step', i, ' finished')

    df_total_areas = pd.DataFrame(df_step)
    df_step_csv_name_list = basedir, '0_post_processing_output/', exp_date, '_', well_loc, 't', time_list[i], 'c2', '_post_processing', '.csv'
    total_areas_csv_name_list_2  =''.join(df_step_csv_name_list)
    df_total_areas.to_csv(total_areas_csv_name_list_2, index=False, header=True)

    t_after_step = time.time()

    t_tot_step = t_after_step - t_before_step

    print('Time for step', i, t_tot_step)



t_after = time.time()

t_tot = t_after - t_before

print('Total time to run', t_tot)