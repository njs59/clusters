import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import glob
from PIL import Image
import time
import matplotlib.animation as animation
from matplotlib.colors import LogNorm
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
well_loc = 's12'

plot_hist = True

num_clusters = []
cluster_areas = np.array([])



cluster_2D_areas_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, '_cluster_areas', '.csv'
cluster_2D_areas_csv_name_list_2  =''.join(cluster_2D_areas_csv_name_list)
df_clus_areas = pd.read_csv(cluster_2D_areas_csv_name_list_2, header=None)
cluster_2D_areas = df_clus_areas.to_numpy()

mean_areas_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, '_mean_areas', '.csv'
mean_areas_csv_name_list_2  =''.join(mean_areas_csv_name_list)
df_mean_areas = pd.read_csv(mean_areas_csv_name_list_2, header=None)
mean_areas = df_mean_areas.to_numpy()

total_areas_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, '_total_areas', '.csv'
total_areas_csv_name_list_2  =''.join(total_areas_csv_name_list)
df_total_areas = pd.read_csv(total_areas_csv_name_list_2, header=None)
total_areas = df_total_areas.to_numpy()

plt.plot(mean_areas/189)
plt.title("Mean Areas")
plt.savefig(basedir + 'clusters/data_analysis/pre-processing/Mean_areas_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()

plt.plot(total_areas/189)
plt.title("Total 2D area")
plt.savefig(basedir + 'clusters/data_analysis/pre-processing/Total_2D_cell_area_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()

cluster_3D_area = (4/3)*pi*((sqrt(cluster_2D_areas/(189*pi)))**3)

tot_3D_volume = []
mean_3D_volume = []
for p in range(len(time_array)):
    time_3D = cluster_3D_area[p,:]
    tot_3D_volume = np.append(tot_3D_volume,sum(time_3D))
    time_3D[time_3D == 0] = np.nan
    mean_curr = np.nanmean(time_3D)
    mean_3D_volume = np.append(mean_3D_volume,mean_curr)

plt.plot(tot_3D_volume)
plt.title("Total 3D Volume")

plt.savefig(basedir + 'clusters/data_analysis/pre-processing/Total_3D_Number_cells_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()

plt.plot(mean_3D_volume)
plt.savefig(basedir + 'clusters/data_analysis/pre-processing/Mean_volume_cluster_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()


if plot_hist == True:

    for i in range(len(time_array)):

        area_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '_area', '.csv'
        area_csv_name_list_2  =''.join(area_csv_name_list)
        df_slice = pd.read_csv(area_csv_name_list_2, header=None)
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

        my_cmap = mpl.colormaps['spring']
        my_cmap.set_under('w')
        plt.imshow(current_array, cmap=my_cmap, norm = LogNorm(vmin=150, vmax=25000))
        # plt.imshow(area_slice, cmap=my_cmap, norm=matplotlib.colors.LogNorm(vmin=100,vmax=25000))
        plt.axis([0, current_array.shape[1], 0, current_array.shape[0]])
        plt.colorbar()
        plt.savefig(f'{basedir}images/cluster_sizes_log/frame-{i:03d}.png', bbox_inches='tight', dpi=300)
        plt.clf()
        

##################################
    

    # create an empty list called images
    images = []

    # get the current time to use in the filename
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # get all the images in the 'images for gif' folder
    for filename in sorted(glob.glob(basedir + 'images/cluster_sizes_log/frame-*.png')): # loop through all png files in the folder
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
    images[0].save(basedir + 'images/cluster_sizes_log/cluster_sizes' + timestr + '.gif',
                save_all=True, append_images=images[1:], optimize=False, duration=300, loop=0)

    # for file in glob.glob(basedir + 'images/frame-*.png'):  # Delete images after use
    #         os.remove(file)
    print('Number of clusters:', num_clusters)
    plt.plot(num_clusters)
    plt.show()


    for j in range(len(time_list)):
        plt.hist(cluster_areas[j,:], bins=[0, 1000, 2000, 3000, 4000, 6000, 8000, 10000, 12000, 16000, 20000, 25000])
        plt.ylim(0, 100) 
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
    images_hist[0].save(basedir + 'images/histogram/' + timestr + '.gif',
                save_all=True, append_images=images_hist[1:], optimize=False, duration=500, loop=0)




