import numpy as np
import matplotlib.pyplot as plt

import skimage.data as data
import skimage.segmentation as seg
from skimage import filters
from skimage import draw
from skimage import color
from skimage import exposure

import read_tif_file_operator as tif

def image_show(image):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()


###    -----------   Input parameters   --------------     ###
basedir = '/Users/Nathan/Documents/Oxford/DPhil/In_vitro_homogeneous_data/'
experiment = 'RAW_data/2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
fileID = '.tif'
time = 71
well_loc = 's09'




raw_arr_2D = tif.tif_to_arr(basedir, experiment, folder, well_loc, time, fileID)


# text = data.page()
image_show(raw_arr_2D)

text_threshold = filters.threshold_otsu  # Hit tab with the cursor after the underscore, try several methods
thresh = text_threshold(raw_arr_2D)
array = raw_arr_2D > thresh
image_show(raw_arr_2D > thresh)