import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image

import matplotlib.animation as animation
from IPython import display

import pre_pro_operators as pre_oper

basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
experiment = '2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03_'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
folder_3 = 'sphere_timelapse/'
fileID = '.tif'

time_array = range(31,98)

time_list = [str(x).zfill(2) for x in time_array]
well_loc = 's12'

cluster_2D_areas_csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, '_cluster_areas', '.csv'
cluster_2D_areas_csv_name_list_2  =''.join(cluster_2D_areas_csv_name_list)
df_clus_areas = pd.read_csv(cluster_2D_areas_csv_name_list_2, header=None)
cluster_areas = df_clus_areas.to_numpy()

number_of_frames = len(time_list)
data = cluster_areas

start_data = time_array[0] - 1

data_times = data[start_data:,]
fig = plt.figure()
plt.axis([150,25000,0,200])
hist = plt.hist(data_times[0], bins=[200, 600, 1000, 2000, 4000, 8000, 16000, 25000])

animation = animation.FuncAnimation(fig, pre_oper.update_hist, number_of_frames, interval=500, fargs=(data_times, ) )


# Save the animation to gif
animation.save(basedir + 'images/histograms/hist' + '.gif', fps=10)


# Show each frame in the gif
im = Image.open(basedir + 'images/histograms/hist' + '.gif')
im.show()
