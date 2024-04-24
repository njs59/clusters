import math
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

def hist_size_plotter(basedir, exp_type, exp_date, multi_loc, start_time, end_time, timestep):
    for i in range(start_time, end_time + 1, timestep):
        cluster_areas = []
        cluster_number = []
        for j in range(len(multi_loc)):
            well_loc = multi_loc[j]
            df_step_csv_name_list = basedir, exp_type, 'post_processing_output/' , exp_date, '/', well_loc, 't', str(i).zfill(2) , 'c2_post_processing', '.csv'
            df_step_csv_name_list_2  =''.join(df_step_csv_name_list)
            df_step = pd.read_csv(df_step_csv_name_list_2)


            cluster_areas_well_ID = df_step["Cluster size"]

            cluster_areas = np.append(cluster_areas, cluster_areas_well_ID)

        cluster_number = cluster_areas/189
        plt.hist(cluster_number)
        plt.show()
        # cluster_number_2D = np.round(cluster_number)
        # plt.hist(cluster_number_2D)
        # plt.show()

        # cluster_radius = np.sqrt(cluster_areas/math.pi)
        # cluster_volume_3D = (4/3)*math.pi*(cluster_radius**3)

        # single_cell_volume = (4/3)*math.pi*((189/math.pi)**(3/2))
        # cluster_number_3D = np.round(cluster_volume_3D/single_cell_volume)

        # chance_of_cell_in_clus = 

        # plt.hist(cluster_number_2D)
        # plt.show()

        # plt.hist(cluster_number_3D)
        # plt.show()