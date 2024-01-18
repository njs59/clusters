import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


from pylab import *
from scipy.ndimage import *

import read_tif_file as tif
import pre_pro_operators as pre_oper

t_before = time.time()


########### Input parameters ##################

basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
experiment = '2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03_'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
folder_3 = 'sphere_timelapse/'
fileID = '.tif'

time_array = range(71,74)

# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(2) for x in time_array]
# time_list= ['21','22','23','24','25','26','27','28','29','30']

well_loc = 's11'

threshold = 0.66
min_clus_size = 20
use_existing_file = False

#################################################


# Function to update indexed array to array displaying areas
def update_arr(arr):
    global area_new, index_keep
    index = np.where(index_keep == arr)
    if len(index[0]) != 0:        
        i = area_new[index[0]][0]
    else:
        i = 0
    return i


################### Code from tif file to txt file ###########################

if use_existing_file == False:
    # Convert tif file to 3D array with values between 0 and 1 (1 is maximum intensity point)
    # ? Problem with thresholding, need constant value not constant proportion
    # Might be ok as we're doing it over whole 3D array so probably ok
    raw_arr_3D = tif.tif_to_arr(basedir, experiment, folder, well_loc, time_list, fileID)

    # Threshold 3D array to boolean array
    tf_bool_3D = pre_oper.threshold_arr(raw_arr_3D, threshold)

    # print(tf_bool_3D)
    print(tf_bool_3D.shape)

else:
    # retrieving data from file.
    loaded_arr = np.loadtxt("/Users/Nathan/Documents/Oxford/DPhil/test_3D.txt")
    
    tf_bool_3D = loaded_arr.reshape(
        loaded_arr.shape[0], loaded_arr.shape[1] // len(time_list), len(time_list))
    
    # check the shapes:
    print("shape of arr: ", tf_bool_3D.shape)



######### Adapt array ################
t_mid = time.time()

cluster_areas = np.array([])

for i in range(len(time_array)):

    t_step_before = time.time()

    current_array_holes = tf_bool_3D[:,:,i]

    current_array = binary_fill_holes(current_array_holes).astype(int)

    label_arr, num_clus = label(current_array)

    plt.imshow(label_arr, interpolation=None)
    plt.show()

    area_list = sum(current_array, label_arr, index=arange(label_arr.max() + 1))

    area_arr = label_arr

    global area_new, index_keep
    area_new, index_keep = pre_oper.remove_fragments(area_list, num_clus, min_clus_size)

    applyall = np.vectorize(update_arr)
    area_slice = applyall(area_arr)
    plt.imshow(area_slice, interpolation=None)
    plt.show()

    ##### Re-binarize array
    slice_binary = np.where(area_slice>0)

    output_label_arr, nc = label(slice_binary)


 
    df_area = pd.DataFrame(area_slice)
    area_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '_area', '.csv'
    area_csv_name_list_2  =''.join(area_csv_name_list)
    df_area.to_csv(area_csv_name_list_2, index=False, header=False)

    df_index = pd.DataFrame(area_slice)
    area_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '_indexed', '.csv'
    area_csv_name_list_2  =''.join(area_csv_name_list)
    df_index.to_csv(area_csv_name_list_2, index=False, header=False)

    t_step_after = time.time()

    t_step = t_step_after - t_step_before

    print('Time for step', i, t_step)



t_after = time.time()

t_tot = t_after - t_before
t_arr_manip = t_after - t_mid

print('Total time to run', t_tot)
print('Time from 3D array to final output', t_arr_manip)

    