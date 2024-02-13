import csv
import numpy as np
import pandas as pd
import time

import matplotlib.pyplot as plt

from scipy.ndimage import *

import post_pro_operators as post_oper

t_before = time.time()

###    -----------   Input parameters   --------------     ###
basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_date = '2017-02-03'
time_array = range(1,98)
# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(2) for x in time_array]
well_loc = 's11'

# Column titles to be used in dataframes
cols = ["Tag number", "Cluster size", "Cluster Centre x", "Cluster Centre y", 
           "Event", "Clusters in event", "Timestep", "Date", "Well ID"]


# Variable to store next tag ID number
next_available_tag = 1

# Loop over each time
for i in range(len(time_list)):

    t_before_step = time.time()

    # Read in area array for given time
    csv_name_list = basedir, 'csv_folder/', exp_date, '_sphere_timelapse_', well_loc, 't', time_list[i], 'c2_area', '.csv'
    csv_name_list_2  =''.join(csv_name_list)
    df_area = pd.read_csv(csv_name_list_2, header=None)
    array_area_current_time = df_area.to_numpy()

    # Read in index array for given time
    csv_name_list_index = basedir, 'csv_folder/', exp_date, '_sphere_timelapse_', well_loc, 't', time_list[i], 'c2_indexed', '.csv'
    csv_name_list_2_index  =''.join(csv_name_list_index)
    df_index = pd.read_csv(csv_name_list_2_index, header=None)
    array_index_current_time = df_index.to_numpy()

    # Initialise dataframe for given time
    df_step = pd.DataFrame(np.nan, index=range(array_index_current_time.max()), columns=cols)
    df_step["Event"] = ""
    df_step["Clusters in event"] = ""

    # Calculate the centres of the clusters (to nearest integer value in x,y)
    centres_2D_current = post_oper.calc_clus_centre(array_index_current_time)

    # Generate 1D array of cluster areas
    area_2D_current = []
    for j in range(1,array_index_current_time.max()+1):
        # Find location for each cluster at current time
        loc_x = np.where(array_index_current_time==j)[0][0]
        loc_y = np.where(array_index_current_time==j)[1][0]
        # Append the list of areas using the area array
        area_2D_current.append(array_area_current_time[loc_x,loc_y])

    # Initial timestep treated differently
    if i == 0:
        # Create list of tagged indices
        tag_number_current = range(1,array_index_current_time.max()+1)

        # Store variables for use in next step
        centres_2D_old = centres_2D_current
        next_available_tag = array_index_current_time.max()+1

    else:
        
        tag_number_current = []
        no_same_locs_index = []
        for k in range(1,array_index_current_time.max()+1):
            same_locs, same_locs_store = post_oper.previous_clusters_at_loc(array_index_current_time, centres_2D_old, k)

            if same_locs == 1:
                #Simple, it's just movement
                # print('Move')
                mask = (df_old['Cluster Centre x'] == same_locs_store[0]) & (df_old['Cluster Centre y'] == same_locs_store[1])
                matching_row = df_old[mask]

                cluster_tag_number = matching_row['Tag number'].tolist()[0]
                tag_number_current.append(cluster_tag_number)
                old_tags_list = list(old_tags_list)
                old_tags_list.remove(cluster_tag_number)
                # print('Yay 2')

                df_step.iloc[k-1,4] = 'Move'
                # df_step.iloc[k-1,5] = str([0])

            elif same_locs == 0:
                # Splitting
                # print('Split')
                no_same_locs_index.append(k)
                tag_number_current.append(next_available_tag)
                next_available_tag += 1
                


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
                old_tags_list = list(old_tags_list)
                for t in range(len(clusters_in_event)):
                    old_tags_list.remove(clusters_in_event[t])

                df_step.iloc[k-1,4] = 'Coagulation'
                df_step.iloc[k-1,5] = str(clusters_in_event)

                tag_number_current.append(cluster_tag_number)
        


        # same_locs = 0 case
        # Splitting code
        # print('Split')
        non_assigned_cluster_array = np.zeros([array_index_old.shape[0], array_index_old.shape[1]])
        locs_not_considered = 0
        for m in range(len(old_tags_list)):
            old_locs_of_arrs = np.where(array_index_old == old_tags_list[m]) 
            if old_locs_of_arrs[0].shape[0] != 0:
                for n in range(len(old_locs_of_arrs[0])):
                    non_assigned_cluster_array[old_locs_of_arrs[0][n], old_locs_of_arrs[1][n]] = array_index_old[old_locs_of_arrs[0][n], old_locs_of_arrs[1][n]]
            
        
        for l in range(len(no_same_locs_index)): 

            index_of_interest = no_same_locs_index[l]           
            search_radius = 50

            x_cen = int(centres_2D_current[index_of_interest-1][0])
            y_cen = int(centres_2D_current[index_of_interest-1][1])

            # Compares with previous timestep array
            near_clus, clus_distances = post_oper.nearby_clusters(x_cen, y_cen, search_radius, array_index_old)
            near_non_assigned_clus, clus_distances_non_assigned = post_oper.nearby_clusters(x_cen, y_cen, search_radius, non_assigned_cluster_array)


            if len(near_clus) == 0:
                # Appearence code
                print('No nearby clusters')
                # Check if cluster at edge of field of view
                if x_cen < 10 or x_cen > 1015 or y_cen < 10 or y_cen > 1334:
                    #cluster at edge 
                    df_step.iloc[index_of_interest-1,4] = 'Edge Appearance'
                    
                else:
                    df_step.iloc[index_of_interest-1,4] = 'Appearance'
                    

            else:
                # search for non-assigned clusters
                if len(near_non_assigned_clus) == 1:
                    # Solo non-assigned cluster
                    # Large move event if close in size else split
                    # Keeps ID of old cluster
                    cluster_index_split_from = post_oper.pick_cluster_inverse_dist(near_non_assigned_clus, clus_distances_non_assigned)
                    cluster_ID = df_old.iloc[cluster_index_split_from - 1 , 0]
                    old_cluster_size = df_old.iloc[cluster_index_split_from - 1 , 1]
                    new_cluster_size = area_2D_current[index_of_interest-1]
                    percent_diff = 100*(abs(new_cluster_size - old_cluster_size))/((old_cluster_size+new_cluster_size)/2)
                    if percent_diff < 20:
                        # Keeps ID of old cluster
                        tag_number_current[no_same_locs_index[l]-1] = cluster_ID
                        df_step.iloc[index_of_interest-1,4] = 'Move large'
                        df_step.iloc[index_of_interest-1,5] = str([cluster_ID])
                    elif old_cluster_size > new_cluster_size:
                        df_step.iloc[index_of_interest-1,4] = 'Splitting'
                        df_step.iloc[index_of_interest-1,5] = str([cluster_ID])
                    else:
                        df_step.iloc[index_of_interest-1,4] = 'Appearance'
                
                elif len(near_non_assigned_clus) > 1:

                    rows_to_save = []
                    for s in range(len(near_non_assigned_clus)):
                        mask = (df_old['Tag number'] == near_non_assigned_clus[s])
                        rows_to_save.append(np.where(mask == True)[0][0])
                    
                    
                    
                    clusters_coagulating = df_old.iloc[rows_to_save]
                    max_near_non_assigned_size = max(clusters_coagulating['Cluster size'])
                    new_cluster_size = area_2D_current[index_of_interest-1]

                    if max_near_non_assigned_size < new_cluster_size:                            
                        cluster_tag_number = min(clusters_coagulating['Tag number'])
                        clusters_in_event = clusters_coagulating['Tag number'].tolist()
                        # for t in range(len(clusters_in_event)):
                            # old_tags_list.remove(clusters_in_event[t])

                        df_step.iloc[k-1,4] = 'Possible Coagulation'
                        df_step.iloc[k-1,5] = str(clusters_in_event)

                        tag_number_current.append(cluster_tag_number)

                    else:
                        # Pick random event with single cluster
                        cluster_index_split_from = post_oper.pick_cluster_inverse_dist(near_non_assigned_clus, clus_distances_non_assigned)
                        cluster_ID = df_old.iloc[cluster_index_split_from - 1 , 0]
                        old_cluster_size = df_old.iloc[cluster_index_split_from - 1 , 1]
                        new_cluster_size = area_2D_current[index_of_interest-1]
                        percent_diff = 100*(abs(new_cluster_size - old_cluster_size))/((old_cluster_size+new_cluster_size)/2)
                        if percent_diff < 20:
                            # Keeps ID of old cluster
                            # Overwrites cluster ID (so is possible for tag to be skipped but that's ok)
                            tag_number_current.append(cluster_ID)
                            df_step.iloc[index_of_interest-1,4] = 'Move large'
                            df_step.iloc[index_of_interest-1,5] = str([cluster_ID])
                        elif old_cluster_size > new_cluster_size:
                            df_step.iloc[index_of_interest-1,4] = 'Splitting'
                            df_step.iloc[index_of_interest-1,5] = str([cluster_ID])

                        else:
                            df_step.iloc[index_of_interest-1,4] = 'Appearance'



                else:
                    # Check if cluster at edge of field of view
                    if x_cen < 10 or x_cen > 1015 or y_cen < 10 or y_cen > 1334:
                        #cluster at edge 
                        df_step.iloc[index_of_interest-1,4] = 'Edge Appearance'


                    else:
                        # Search nearby clusters already assigned

                        # Can only be splitting
                         
                        # (can't move large as that can only happen if there is an unassigned cluster)
                        # Can't be appearence as that has been checked for at the very start
                        cluster_index_split_from = post_oper.pick_cluster_inverse_dist(near_clus, clus_distances)
                        cluster_ID = df_old.iloc[cluster_index_split_from - 1 , 0]
                        df_step.iloc[index_of_interest-1,4] = 'Splitting type 2'
                        df_step.iloc[index_of_interest-1,5] = str([cluster_ID])
            # print('Yay 3')
        
    
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
    old_tags_list = tag_number_current
    array_index_old = array_index_current_time

    print('Yay step', i, ' finished')

    df_total_areas = pd.DataFrame(df_step)
    df_step_csv_name_list = basedir, '0_post_processing_output/', '000_test_attempt', exp_date, '_', well_loc, 't', time_list[i], 'c2', '_post_processing', '.csv'
    total_areas_csv_name_list_2  =''.join(df_step_csv_name_list)
    df_total_areas.to_csv(total_areas_csv_name_list_2, index=False, header=True)

    t_after_step = time.time()

    t_tot_step = t_after_step - t_before_step

    print('Time for step', i, t_tot_step)



t_after = time.time()

t_tot = t_after - t_before

print('Total time to run', t_tot)