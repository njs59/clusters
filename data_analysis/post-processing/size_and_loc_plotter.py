import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def size_and_loc_tracker(start_time, end_time, timejump,  basedir, exp_type, exp_date, well_loc, cluster_lineage):
    '''
Cluster tracker tracks an individually taggged cluster over time
Input arguments: 
    start_time: first timepoint to plot
    end_time: final timepoint to plot
    timejump: number of timesteps between each plot
    cluster_index_final_time: row in final time to select cluster ID tag from
    basedir,
    exp_type,
    exp_date,
    well_loc

Output:
    Series of plots 
'''
    if len(cluster_lineage) > 0:
        cluster_tags = cluster_lineage
    else:
        df_end_csv_name_list = basedir, exp_type, 'post_processing_output/' , exp_date, '/', well_loc, 't', str(end_time).zfill(2) , 'c2_post_processing', '.csv'
        df_end_csv_name_list_2  =''.join(df_end_csv_name_list)
        df_end = pd.read_csv(df_end_csv_name_list_2)

        cluster_tags = df_end["Tag number"].to_numpy().astype(int)



    for h in range(len(cluster_tags)):

        cluster_tag_to_track = cluster_tags[h]

        x = []
        cluster_size = []
        cluster_location_x = []
        cluster_location_y = []

        for i in range(start_time - 1, end_time, timejump):
            x = np.append(x, i)
            # Read in csv
            time_i = str(i).zfill(2)
            index_csv_name_list = basedir, exp_type, 'pre_processing_output/', exp_date, '/', well_loc, 't', time_i, 'c2', '_indexed', '.csv'
            index_csv_name_list_2  =''.join(index_csv_name_list)
            df_slice = pd.read_csv(index_csv_name_list_2, header=None)
            current_array = df_slice.to_numpy()

            df_storage_csv_name_list = basedir, exp_type, 'post_processing_output/', exp_date, '/', well_loc, 't', time_i , 'c2_post_processing', '.csv'
            df_storage_csv_name_list_2  =''.join(df_storage_csv_name_list)
            df_storage = pd.read_csv(df_storage_csv_name_list_2)

            
            cluster_current_row_of_interest = df_storage.loc[df_storage['Tag number'] == cluster_tag_to_track]
            # Store centres in array
            if cluster_current_row_of_interest.shape[0] == 0:
                cluster_size = np.append(cluster_size, 0)
                cluster_location_x = np.append(cluster_location_x, None)
                cluster_location_y = np.append(cluster_location_y, None)
                continue
            df1_slice = cluster_current_row_of_interest[['Cluster Centre x', 'Cluster Centre y']]
            centres_end_2D_lineage = df1_slice.to_numpy()

            

            cluster_size = np.append(cluster_size, cluster_current_row_of_interest['Cluster size'])
            cluster_location_x = np.append(cluster_location_x, int(centres_end_2D_lineage[0][0]))
            cluster_location_y = np.append(cluster_location_y, int(centres_end_2D_lineage[0][1]))


        plt.figure(1)
        plt.plot(cluster_location_x, cluster_location_y)
        # plt.show()
        
        plt.figure(2)
        plt.plot(x, cluster_size)

        
        plt.figure(3)
        # fig, ax = plt.subplots()
        for i in range(len(cluster_location_x)-1):
            r = i/len(cluster_location_x)
            if i < len(cluster_location_x)/2:
                b = i/ (len(cluster_location_x)/2)
            else:
                b = 2 - (i/ (len(cluster_location_x)/2))
            print('B is', b)
            g = 1-r
            color = (r, g, b)
            plt.plot(cluster_location_x[i:i+2], cluster_location_y[i:i+2], c=color, lw=2)
            # plt.plot(cluster_location_x, cluster_location_y)
    plt.show()
    plt.show()
    plt.show()
    

        
    
