import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import glob
from PIL import Image
import time
from matplotlib.colors import LogNorm

from pylab import *



### ------------   Input parameters    -----------------  ###
basedir = '/Users/Nathan/Documents/Oxford/DPhil/clusters/worked_example/'
csv_loc = 'data_analysis_outputs/csv_files/'
saving_plot_loc = 'data_analysis_outputs/plots/'

# exp_date = '2017-02-03'
# time_array = range(1,98)
# time_list = [str(x).zfill(2) for x in time_array]
# well_loc = 's11'

exp_date = '2017-03-16'
time_array = range(1,146)
time_list = [str(x).zfill(3) for x in time_array]
# well_loc = 's037'
well_loc = 's074'

# Does the histogram get plotted
plot_hist = True



### -----------------  Plotting code  ----------------- ###

num_clusters = []
cluster_areas = np.array([])


# Read in 2D array of cluster areas over time
cluster_2D_areas_csv_name_list = basedir, csv_loc, exp_date, '/', well_loc, '_cluster_areas', '.csv'
cluster_2D_areas_csv_name_list_2  =''.join(cluster_2D_areas_csv_name_list)
df_clus_areas = pd.read_csv(cluster_2D_areas_csv_name_list_2, header=None)
cluster_2D_areas = df_clus_areas.to_numpy()
print('Shape', cluster_2D_areas.shape)

# Read in mean area of cluster
mean_areas_csv_name_list = basedir, csv_loc, exp_date, '/', well_loc, '_mean_areas', '.csv'
mean_areas_csv_name_list_2  =''.join(mean_areas_csv_name_list)
df_mean_areas = pd.read_csv(mean_areas_csv_name_list_2, header=None)
mean_areas = df_mean_areas.to_numpy()

# Read in total cluster coverage area
total_areas_csv_name_list = basedir, csv_loc, exp_date, '/', well_loc, '_total_areas', '.csv'
total_areas_csv_name_list_2  =''.join(total_areas_csv_name_list)
df_total_areas = pd.read_csv(total_areas_csv_name_list_2, header=None)
total_areas = df_total_areas.to_numpy()

# Read in number of clusters
number_clusters_csv_name_list = basedir, csv_loc, exp_date, '/', well_loc, '_number_clusters', '.csv'
number_clusters_csv_name_list_2  =''.join(number_clusters_csv_name_list)
df_number_clusters = pd.read_csv(number_clusters_csv_name_list_2, header=None)
number_clusters = df_number_clusters.to_numpy()

# Plot mean size of cluster
plt.plot(mean_areas/189)
plt.title("Mean Areas")
plt.savefig(basedir + saving_plot_loc + 'Mean_areas_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()

# Plot total coverage of clusters over array
plt.plot(total_areas/189)
plt.title("Total 2D area")
plt.savefig(basedir + saving_plot_loc + 'Total_2D_cell_area_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()

# Plot number of clusters
plt.plot(number_clusters)
plt.title("Number of clusters over time")
plt.savefig(basedir + saving_plot_loc + 'Number_clusters' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()

# Convert 2D circular areas to 3D spherical volumes
cluster_3D_area = (4/3)*pi*((sqrt(cluster_2D_areas/(189*pi)))**3)

tot_3D_volume = []
mean_3D_volume = []
# Calculate mean and total 3D volumes
for p in range(len(time_array)):
    time_3D = cluster_3D_area[p,:]
    tot_3D_volume = np.append(tot_3D_volume,sum(time_3D))
    time_3D[time_3D == 0] = np.nan
    mean_curr = np.nanmean(time_3D)
    mean_3D_volume = np.append(mean_3D_volume,mean_curr)

# Plot total 3D
plt.plot(tot_3D_volume)
plt.title("Total 3D Volume")
plt.savefig(basedir + saving_plot_loc + 'Total_3D_Number_cells_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()

# Plot mean 3D volume of cluster
plt.plot(mean_3D_volume)
plt.savefig(basedir + saving_plot_loc + 'Mean_volume_cluster_' + well_loc + '.png', dpi=300)
# plt.show()
plt.clf()


### ---------------   Code to generate gif of clusters over time   ---------------------- ###

# Create plot for each timepoint
for i in range(len(time_array)):

    # Read in area array at current time
    area_csv_name_list = basedir, csv_loc, exp_date, '/', well_loc, 't', time_list[i], 'c2', '_area', '.csv'
    area_csv_name_list_2  =''.join(area_csv_name_list)
    df_slice = pd.read_csv(area_csv_name_list_2, header=None)
    current_array = df_slice.to_numpy()

    # Plot a heatmap of the array on a log scale and savre the image for use in a gif
    my_cmap = mpl.colormaps['spring']
    my_cmap.set_under('w')
    plt.imshow(current_array, cmap=my_cmap, norm = LogNorm(vmin=150, vmax=25000))
    # plt.imshow(area_slice, cmap=my_cmap, norm=matplotlib.colors.LogNorm(vmin=100,vmax=25000))
    plt.axis([0, current_array.shape[1], 0, current_array.shape[0]])
    plt.colorbar()
    plt.savefig(f'{basedir + saving_plot_loc}gif_frames/frame-{i:03d}.png', bbox_inches='tight', dpi=300)
    plt.clf()
    

###   -----------------  Gif code  ----------------- ###

# create an empty list called images
images = []

# get the current time to use in the filename
timestr = time.strftime("%Y%m%d-%H%M%S")

# get all the images in the 'images for gif' folder
for filename in sorted(glob.glob(basedir + saving_plot_loc + 'gif_frames/frame-*.png')): # loop through all png files in the folder
    im = Image.open(filename) # open the image
    images.append(im) # add the image to the list

# calculate the frame number of the last frame (ie the number of images)
last_frame = (len(images)) 

# create 10 extra copies of the last frame (to make the gif spend longer on the most recent data)
for x in range(0, 9):
    im = images[last_frame-1]
    images.append(im)

# save as a gif   
images[0].save(basedir + saving_plot_loc + 'gif_' + timestr + '.gif',
            save_all=True, append_images=images[1:], optimize=False, duration=300, loop=0)

## Code to remove constituent images if not wanting to store
# for file in glob.glob(basedir + 'images/frame-*.png'):  # Delete images after use
#         os.remove(file)



###   ---------------   Histogram plotting code   --------------------   ###
if plot_hist == True:
    # Plot and store histogram images at each timepoint for use in a gif
    for j in range(len(time_list)):
        plt.hist(cluster_2D_areas[j,:], bins=[0, 1000, 2000, 3000, 4000, 6000, 8000, 10000, 12000, 16000, 20000, 25000])
        plt.ylim(0, 100) 
        plt.savefig(f'{basedir +  saving_plot_loc}hist_frames/frame-{j:03d}.png', bbox_inches='tight', dpi=300)
        plt.clf()

    images_hist = []
    # get all the images in the 'images for gif' folder
    for filename_hist in sorted(glob.glob(basedir + saving_plot_loc + 'hist_frames/frame-*.png')): # loop through all png files in the folder
        im_hist = Image.open(filename_hist) # open the image
        images_hist.append(im_hist) # add the image to the list

    # calculate the frame number of the last frame (ie the number of images)
    last_frame = (len(images_hist)) 

    # create 10 extra copies of the last frame (to make the gif spend longer on the most recent data)
    for x in range(0, 9):
        im_hist = images_hist[last_frame-1]
        images_hist.append(im_hist)

    # save as a gif   
    images_hist[0].save(basedir + saving_plot_loc + 'histogram_' + timestr + '.gif',
                save_all=True, append_images=images_hist[1:], optimize=False, duration=500, loop=0)

