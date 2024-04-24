import glob
from PIL import Image
import time

import matplotlib.pyplot as plt

import read_tif_file_operator as tif


###    -----------   Input parameters   --------------     ###
basedir = '/Users/Nathan/Documents/Oxford/DPhil/In_vitro_homogeneous_data/'
experiment = 'RAW_data/2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03'
# experiment = 'RAW_data/2017-02-13_sphere_timelapse_2/'
# exp_date = '2017-02-13'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
fileID = '.tif'
time_list = range(42,98,5)
well_loc = 's11'

# get the current time to use in the filename
timestr = time.strftime("%Y%m%d-%H%M%S")

# Plot and store histogram images at each timepoint for use in a gif
for j in range(len(time_list)):
    raw_arr_2D = tif.tif_to_arr(basedir, experiment, folder, well_loc, str(time_list[j]), fileID)

    plt.hist(raw_arr_2D)
    plt.xlim(300, 600) 
    plt.savefig(f'/Users/Nathan/Documents/Oxford/DPhil/clusters/data_analysis/pre-processing/test_code/histogram/frame-{j:03d}.png', bbox_inches='tight', dpi=300)
    plt.clf()

images_hist = []
# get all the images in the 'images for gif' folder
for filename_hist in sorted(glob.glob('/Users/Nathan/Documents/Oxford/DPhil/clusters/data_analysis/pre-processing/test_code/histogram/frame-*.png')): # loop through all png files in the folder
    im_hist = Image.open(filename_hist) # open the image
    images_hist.append(im_hist) # add the image to the list

# calculate the frame number of the last frame (ie the number of images)
last_frame = (len(images_hist)) 

# create 10 extra copies of the last frame (to make the gif spend longer on the most recent data)
for x in range(0, 9):
    im_hist = images_hist[last_frame-1]
    images_hist.append(im_hist)

# save as a gif   
images_hist[0].save('/Users/Nathan/Documents/Oxford/DPhil/clusters/data_analysis/pre-processing/test_code/histogram/' + timestr + '.gif',
            save_all=True, append_images=images_hist[1:], optimize=False, duration=500, loop=0)

