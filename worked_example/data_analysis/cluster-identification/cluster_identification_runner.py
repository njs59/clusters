import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from osgeo import gdal as GD

from pylab import *
from scipy.ndimage import *

import read_tif_file_operator as tif
import cluster_identification_operators as iden_oper

t_before = time.time()


###    -----------   Input parameters   --------------     ###
# basedir = '/Users/Nathan/Documents/Oxford/DPhil/In_vitro_homogeneous_data/'
# experiment = 'RAW_data/2017-02-03_sphere_timelapse/'
# experiment_data = '2017-02-03 sphere timelapse/'
# exp_date = '2017-02-03'
# folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
# folder_data = 'RAW/Timelapse/sphere_timelapse/'
# folder_3 = ''
# fileID = '.tif'
# time_array = range(1,98)
# # Rename single digit values with 0 eg 1 to 01 for consistency
# time_list = [str(x).zfill(2) for x in time_array]
# well_loc = 's10'
# naming_convention_pre_number = basedir, experiment, folder, 'sphere_timelapse_', well_loc, 't'
# naming_convention_post_number = 'c2', '_ORG', fileID
# file_saving_folder = '/Users/Nathan/Documents/Oxford/DPhil/clusters/data_analysis_outputs/'


basedir = '/Volumes/Elements/Nate thesis data/Thesis Data/'
experiment = '2017-03-16 sphere TL 6/'
exp_date = '2017-03-16'
folder = 'RAW/2017-03-16 sphere TL 6/2017-03-13 sphere TL 6-03/'
folder_3 = 'sphere_timelapse/'
fileID = '.tif'
time_array = range(1,146)
# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(3) for x in time_array]
# well_loc = 's037'
well_loc = 's074'
naming_convention_pre_number = basedir, experiment, folder, '2017-03-13 sphere TL 6-03_', well_loc, 't'
naming_convention_post_number = 'c2', '_ORG', fileID

file_saving_folder = '/Users/Nathan/Documents/Oxford/DPhil/clusters/data_analysis_outputs/'




min_clus_size = 150
use_existing_file = False

###  ------------  End of input parameters  --------------  ###
###############################################################


# Function to update indexed array to array displaying areas
def calc_area_arr(arr):
    global area_new, index_keep
    index = np.where(index_keep == arr)
    if len(index[0]) != 0:        
        i = area_new[index[0]][0]
    else:
        i = 0
    return i

### -------------------   Module 1: Identification      ---------------------  ###

    ##  ------ Code from tif file to txt file  -- ##

if use_existing_file == False:
    # Convert tif file to 3D array with values between 0 and 1 (1 is maximum intensity point)
    raw_arr_3D = tif.tif_to_arr(naming_convention_pre_number, naming_convention_post_number, time_list)
    
    # Threshold 3D array to boolean array
    tf_bool_3D = iden_oper.threshold_arr_unsupervised(raw_arr_3D)
    print(tf_bool_3D.shape)


### ----------------- Code to skip Module 1 if previously run  --------------------- ###

else:
    # retrieving data from file.
    loaded_arr = np.loadtxt("/Users/Nathan/Documents/Oxford/DPhil/current_tiff.txt")
    
    tf_bool_3D = loaded_arr.reshape(
        loaded_arr.shape[0], loaded_arr.shape[1] // len(time_list), len(time_list))
    
    # check the shapes:
    print("shape of arr: ", tf_bool_3D.shape)


### -------------------   Module 2: Manipulation and storage      ---------------------  ###
    
    ## ------ Code from txt file to storage .csv files for area and index -- ##

t_mid = time.time()

cluster_areas = np.array([])
fig_1 = plt.figure()
num_clusters = []
total_area = []
mean_area = []

# Loop over all timepoint to get outputs for each timepoint
for i in range(len(time_array)):

    t_step_before = time.time()

    current_array_holes = tf_bool_3D[:,:,i]  # Get 2D boolean array for current time

    # Fill any single pixel holes in clusters
    current_array = binary_fill_holes(current_array_holes).astype(int) 

    # Label the clusters of the boolean array
    label_arr, num_clus = label(current_array)

    # plt.imshow(label_arr, interpolation=None)
    # plt.show()

    # Get a 1D list of areas of the clusters
    area_list = sum(current_array, label_arr, index=arange(label_arr.max() + 1))

    area_arr = label_arr

    global area_new, index_keep
    # Remove fragments, that is clusters smaller than
    # min_clus_size so we only consider clusters large enough
    # to be a cell rather than a cell fragment
    area_new, index_keep = iden_oper.remove_fragments(area_list, num_clus, min_clus_size)

    # Calculate and store total area now in clusters, number of clusters and mean cluster area 
    total_curr_area = np.sum(area_new)
    print('Total current area', total_curr_area)
    mean_curr_area = np.mean(area_new)
    print('Mean cluster area', mean_curr_area)
    num_clusters = np.append(num_clusters,len(area_new))
    total_area = np.append(total_area, np.sum(area_new))
    mean_area = np.append(mean_area, np.mean(area_new))

    # Calculate 2D cluster array with cluster areas rather than indeces
    applyall = np.vectorize(calc_area_arr)
    area_slice = applyall(area_arr)

    # Plot area array heatmap on a log scale and save figure
    my_cmap = mpl.colormaps['spring']
    my_cmap.set_under('k')
    plt.imshow(area_slice, cmap=my_cmap, vmin=1)
    plt.axis([0, area_slice.shape[1], 0, area_slice.shape[0]])
    plt.colorbar()
    plt.savefig(f'{basedir}images/frame-{i:03d}.png', bbox_inches='tight', dpi=300)
    plt.clf()

    

    ##### Re-binarize (to boolean) and label array to output updated index array after fragments removed
    slice_binary = np.array(area_slice, dtype=bool).astype(int)
    output_label_arr, nc = label(slice_binary)


    # Save area array to csv file
    df_area = pd.DataFrame(area_slice)
    area_csv_name_list = file_saving_folder, 'csv_files/', exp_date, '/', well_loc, 't', time_list[i], 'c2', '_area', '.csv'
    area_csv_name_list_2  =''.join(area_csv_name_list)
    df_area.to_csv(area_csv_name_list_2, index=False, header=False)

    # Save index array to csv file
    df_index = pd.DataFrame(output_label_arr)
    index_csv_name_list = file_saving_folder, 'csv_files/', exp_date, '/', well_loc, 't', time_list[i], 'c2', '_indexed', '.csv'
    index_csv_name_list_2  =''.join(index_csv_name_list)
    df_index.to_csv(index_csv_name_list_2, index=False, header=False)

    # Add the cluster areas to 2D array of cluster sizes over time (for histogram plotting)
    cluster_areas = iden_oper.save_clus_areas(i, area_new, cluster_areas)


    t_step_after = time.time()
    t_step = t_step_after - t_step_before
    print('Time for step', i, t_step)


t_after = time.time()

t_tot = t_after - t_before
t_arr_manip = t_after - t_mid

print('Total time to run', t_tot)
print('Time from 3D array to final output', t_arr_manip)

print('Shapes', cluster_areas.shape, mean_area.shape, total_area.shape)


### -----------------   Outputs and initial plots ------------------------- ###

# Save 2D cluster areas array to csv
df_cluster_areas = pd.DataFrame(cluster_areas)
cluster_areas_csv_name_list = file_saving_folder, 'csv_files/', exp_date, '/', well_loc, '_cluster_areas', '.csv'
cluster_areas_csv_name_list_2  =''.join(cluster_areas_csv_name_list)
df_cluster_areas.to_csv(cluster_areas_csv_name_list_2, index=False, header=False)

# Save mean areas to csv
df_mean_areas = pd.DataFrame(mean_area)
mean_areas_csv_name_list = file_saving_folder, 'csv_files/', exp_date, '/', well_loc, '_mean_areas', '.csv'
mean_areas_csv_name_list_2  =''.join(mean_areas_csv_name_list)
df_mean_areas.to_csv(mean_areas_csv_name_list_2, index=False, header=False)

# Save total areas to csv
df_total_areas = pd.DataFrame(total_area)
total_areas_csv_name_list = file_saving_folder, 'csv_files/', exp_date, '/', well_loc, '_total_areas', '.csv'
total_areas_csv_name_list_2  =''.join(total_areas_csv_name_list)
df_total_areas.to_csv(total_areas_csv_name_list_2, index=False, header=False)

# Save number of clusters to csv
df_number_clusters = pd.DataFrame(num_clusters)
number_clusters_csv_name_list = file_saving_folder, 'csv_files/', exp_date, '/', well_loc, '_number_clusters', '.csv'
number_clusters_csv_name_list_2  =''.join(number_clusters_csv_name_list)
df_number_clusters.to_csv(number_clusters_csv_name_list_2, index=False, header=False)
    