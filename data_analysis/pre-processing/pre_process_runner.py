from osgeo import gdal as GD
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
from skimage import io
from PIL import Image

from pylab import *
from scipy.ndimage import *

import read_tif_file as tif
import pre_pro_operators as pre_oper

basedir = '/Users/Nathan/Documents/Oxford/DPhil/'


experiment = '2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03_'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
folder_3 = 'sphere_timelapse/'

fileID = '.tif'

time_array = range(21,31)

time_list = [str(x).zfill(2) for x in time_array]
# time_list= ['21','22','23','24','25','26','27','28','29','30']

well_loc = 's11'

threshold = 0.66
min_clus_size = 20
use_existing_file = True



def update_arr(arr):
    global area_new, index_keep
    index = np.where(index_keep == arr)
    if len(index[0]) != 0:        
        i = area_new[index[0]][0]
    else:
        i = 0
    return i


if use_existing_file == False:
    raw_arr_3D = tif.tif_to_arr(basedir, experiment, folder, well_loc, time_list, fileID)


    tf_bool_3D = pre_oper.threshold_arr(raw_arr_3D, threshold)

    print(tf_bool_3D)
    print(tf_bool_3D.shape)

else:
    # retrieving data from file.
    loaded_arr = np.loadtxt("/Users/Nathan/Documents/Oxford/DPhil/test_3D.txt")
    
    tf_bool_3D = loaded_arr.reshape(
        loaded_arr.shape[0], loaded_arr.shape[1] // len(time_list), len(time_list))
    
    # check the shapes:
    print("shape of arr: ", tf_bool_3D.shape)



######### Adapt array ################

for i in range(len(time_array)):

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
    print(area_slice)


 
    df = pd.DataFrame(area_slice)
    csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '.csv'
    csv_name_list_2  =''.join(csv_name_list)
    print(csv_name_list_2)
    df.to_csv(csv_name_list_2)






    