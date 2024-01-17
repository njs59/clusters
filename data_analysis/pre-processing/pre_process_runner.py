from osgeo import gdal as GD
import matplotlib.pyplot as plt
import numpy as np

import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
from skimage import io
from PIL import Image

from pylab import *
from scipy.ndimage import measurements

from scipy.ndimage import *

import read_tif_file as tif
import pre_pro_operators as pre_oper

basedir = '/Users/Nathan/Documents/Oxford/DPhil/'


experiment = '2017-02-03_sphere_timelapse/'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
folder_3 = 'sphere_timelapse/'

fileID = '.tif'

time_array = range(21,31)

time_list = [str(x).zfill(2) for x in time_array]
# time_list= ['21','22','23','24','25','26','27','28','29','30']

well_loc = 's11'

use_existing_file = False

if use_existing_file == False:
    raw_arr_3D = tif.tif_to_arr(basedir, experiment, folder, well_loc, time_list, fileID)

    threshold = 0.66
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