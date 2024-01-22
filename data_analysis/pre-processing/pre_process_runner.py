import copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


import matplotlib.animation as animation
from IPython import display

import glob
import contextlib
import os
from PIL import Image


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

time_array = range(1,98)

# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(2) for x in time_array]
# time_list= ['21','22','23','24','25','26','27','28','29','30']

well_loc = 's11'

threshold = 1.2
min_clus_size = 150
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
fig_1 = plt.figure()
num_clusters = []
for i in range(len(time_array)):

    t_step_before = time.time()

    current_array_holes = tf_bool_3D[:,:,i]

    current_array = binary_fill_holes(current_array_holes).astype(int)

    label_arr, num_clus = label(current_array)

    # plt.imshow(label_arr, interpolation=None)
    # plt.show()

    area_list = sum(current_array, label_arr, index=arange(label_arr.max() + 1))

    area_arr = label_arr

    global area_new, index_keep
    area_new, index_keep = pre_oper.remove_fragments(area_list, num_clus, min_clus_size)

    num_clusters = np.append(num_clusters,len(area_new))

    applyall = np.vectorize(update_arr)
    area_slice = applyall(area_arr)
    my_cmap = mpl.colormaps['spring']
    my_cmap.set_under('k')
    plt.imshow(area_slice, cmap=my_cmap, vmin=1)
    # plt.imshow(area_slice, cmap=my_cmap, norm=matplotlib.colors.LogNorm(vmin=100,vmax=25000))
    plt.axis([0, area_slice.shape[1], 0, area_slice.shape[0]])
    plt.colorbar()
    plt.savefig(f'{basedir}images/frame-{i:03d}.png', bbox_inches='tight', dpi=300)
    plt.clf()

    
    # plt.show()
    # animation_1 = animation.FuncAnimation(fig_1, pre_oper.update_heat_map, len(time_array), interval=500, fargs=(area_slice) )



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

    cluster_areas = pre_oper.save_clus_areas(i, area_new, cluster_areas)


    t_step_after = time.time()

    t_step = t_step_after - t_step_before

    print('Time for step', i, t_step)


# # converting to an html5 video
# video_1 = animation_1.to_html5_video()

# # embedding for the video
# html_1 = display.HTML(video_1)

# # draw the animation
# display.display(html_1)
# plt.show()

t_after = time.time()

t_tot = t_after - t_before
t_arr_manip = t_after - t_mid

print('Total time to run', t_tot)
print('Time from 3D array to final output', t_arr_manip)


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


number_of_frames = len(time_list)
data = cluster_areas
fig = plt.figure()
hist = plt.hist(data[0,:])

animation = animation.FuncAnimation(fig, pre_oper.update_hist, number_of_frames, interval=500, fargs=(data, ) )

# converting to an html5 video
video = animation.to_html5_video()

# embedding for the video
html = display.HTML(video)

# draw the animation
display.display(html)
plt.show()
# plt.close()

    