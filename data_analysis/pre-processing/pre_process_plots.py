import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import glob
from PIL import Image
import time
import matplotlib.animation as animation
from IPython import display

from pylab import *
from scipy.ndimage import *


import pre_pro_operators as pre_oper

basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
experiment = '2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03_'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
folder_3 = 'sphere_timelapse/'
fileID = '.tif'

time_array = range(1,98)

time_list = [str(x).zfill(2) for x in time_array]
well_loc = 's11'


num_clusters = []
cluster_areas = np.array([])

for i in range(len(time_array)):

    area_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '_area', '.csv'
    area_csv_name_list_2  =''.join(area_csv_name_list)
    df_slice = pd.read_csv(area_csv_name_list_2)
    current_array = df_slice.to_numpy()

    ##### Re-binarize array
    slice_binary = (current_array > 0).astype(np.int_)
    # slice_binary = np.where(current_array>0)

    label_arr, num_clus = label(slice_binary)

    # plt.imshow(label_arr, interpolation=None)
    # plt.show()

    area_new = sum(slice_binary, label_arr, index=arange(label_arr.max() + 1))

    num_clusters = np.append(num_clusters,len(area_new))

    cluster_areas = pre_oper.save_clus_areas(i, area_new, cluster_areas)
    

##################################
    

# create an empty list called images
images = []

# get the current time to use in the filename
timestr = time.strftime("%Y%m%d-%H%M%S")

# get all the images in the 'images for gif' folder
for filename in sorted(glob.glob(basedir + 'images/frame-*.png')): # loop through all png files in the folder
    im = Image.open(filename) # open the image
    # im_small = im.resize((1200, 1500), resample=0) # resize them to make them a bit smaller
    images.append(im) # add the image to the list

# calculate the frame number of the last frame (ie the number of images)
last_frame = (len(images)) 

# create 10 extra copies of the last frame (to make the gif spend longer on the most recent data)
for x in range(0, 9):
    im = images[last_frame-1]
    images.append(im)

# save as a gif   
images[0].save(basedir + 'images/cluster_sizes' + timestr + '.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)

# for file in glob.glob(basedir + 'images/frame-*.png'):  # Delete images after use
#         os.remove(file)
print('Number of clusters:', num_clusters)
plt.plot(num_clusters)
plt.show()


for j in range(len(time_list)):
    plt.hist(cluster_areas[j,:], bins=[150, 1000, 2000, 3000, 4000, 6000, 8000, 10000, 12000, 16000, 20000, 25000])
    plt.ylim(0, 300) 
    plt.savefig(f'{basedir}images/histogram/frame-{j:03d}.png', bbox_inches='tight', dpi=300)
    plt.clf()

images_hist = []
# get all the images in the 'images for gif' folder
for filename_hist in sorted(glob.glob(basedir + 'images/histogram/frame-*.png')): # loop through all png files in the folder
    im_hist = Image.open(filename_hist) # open the image
    # im_small = im.resize((1200, 1500), resample=0) # resize them to make them a bit smaller
    images_hist.append(im_hist) # add the image to the list

# calculate the frame number of the last frame (ie the number of images)
last_frame = (len(images_hist)) 

# create 10 extra copies of the last frame (to make the gif spend longer on the most recent data)
for x in range(0, 9):
    im_hist = images_hist[last_frame-1]
    images_hist.append(im_hist)

# save as a gif   
images_hist[0].save(basedir + 'images/histogram/cluster_sizes' + timestr + '.gif',
               save_all=True, append_images=images_hist[1:], optimize=False, duration=500, loop=0)




