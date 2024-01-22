import csv
import numpy as np
import pandas as pd

from scipy.ndimage import *

import post_pro_operators as post_oper


basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_date = '2017-02-03_'
time_array = range(21,31)
# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(2) for x in time_array]
well_loc = 's11'

cols = ["Tag number", "Cluster size", "Cluster centre x", "Cluster Centre y", 
           "Event", "Clusters in event", "Timestep", "Date", "Well ID"]

for i in range(len(time_list)):

    csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '.csv'
    csv_name_list_2  =''.join(csv_name_list)

    df = pd.read_csv(csv_name_list_2)

    array_area_current_time = df.to_numpy()
    
    ##### Re-binarize array
    slice_binary = (array_area_current_time > 0).astype(np.int_)

    label_arr, num_clus = label(slice_binary)

    df_step = pd.DataFrame(np.nan, index=range(num_clus), columns=cols)

    centres_2D_current = post_oper.calc_clus_centre(label_arr)

    area_2D_current = []
    for j in range(1,num_clus+1):
        loc_x = np.where(label_arr==j)[0][0]
        loc_y = np.where(label_arr==j)[1][0]
        area_2D_current.append(array_area_current_time[loc_x,loc_y])

    print(centres_2D_current.shape)
    print(area_2D_current)


    df_step.iloc[:,1] = area_2D_current
    df_step.iloc[:,2] = centres_2D_current[:,0].tolist()
    df_step.iloc[:,3] = centres_2D_current[:,1].tolist()
    df_step.iloc[:,6] = time_list[i]

    print(df_step)

    print('Yay')

    