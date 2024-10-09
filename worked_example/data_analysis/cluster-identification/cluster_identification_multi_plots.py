import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pylab import *



### ------------   Input parameters    -----------------  ###
basedir = '/Users/Nathan/Documents/Oxford/DPhil/clusters/worked_example/'
csv_loc = 'data_analysis_outputs/csv_files/'
saving_plot_loc = 'data_analysis_outputs/plots/'

# exp_date = '2017-02-03'
# time_array = range(1,98)
# time_list = [str(x).zfill(2) for x in time_array]
# multi_well = ['s11', 's12']

exp_date = '2017-03-16'
time_array = range(1,146)
time_list = [str(x).zfill(3) for x in time_array]
# multi_well = ['s037', 's038']
multi_well = ['s073', 's074']
initial_plotting_time = 10
final_plotting_time = 72


plt_num = 0
for i in range(len(multi_well)):
    well_loc = multi_well[i]
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

    ### ----------------  Plotting code  ------------------- ###

    initial_plot_index = 2 * initial_plotting_time
    final_plot_index = 2 * final_plotting_time
    lin_space_num = 2*(final_plotting_time - initial_plotting_time) + 1
    
    x = np.linspace(initial_plot_index, final_plot_index, lin_space_num)

    cm = plt.cm.get_cmap('tab20')
    # Plot mean size of cluster
    plt.figure(1)
    mean_areas = mean_areas/189
    plt.plot(x, mean_areas[initial_plot_index:final_plot_index+1])
    plt.xlim(initial_plotting_time,final_plotting_time)
    plt.ylabel("Number of cells")
    plt.xlabel("time (hours)")
    plt.savefig(basedir + saving_plot_loc + 'INV_Mean_areas_' + 'multi' + '.png', dpi=300, bbox_inches="tight")

    # Plot number of clusters
    plt.figure(2)
    plt.plot(x, mean_areas[initial_plot_index:final_plot_index+1])
    plt.xlim(initial_plotting_time,final_plotting_time)
    plt.ylabel("Number of clusters")
    plt.xlabel("time (hours)")
    plt.savefig(basedir + saving_plot_loc + 'INV_Number_clusters_' + 'multi' + '.png', dpi=300, bbox_inches="tight")

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
    plt.figure(3)
    plt.plot(x, mean_areas[initial_plot_index:final_plot_index+1])
    plt.xlim(initial_plotting_time,final_plotting_time)
    plt.ylim(0,4000)
    plt.ylabel("Number of cells")
    plt.xlabel("time (hours)")
    plt.savefig(basedir + saving_plot_loc + 'INV_Total_3D_Number_cells_' + 'multi' + '.png', dpi=300, bbox_inches="tight")


    # Plot mean 3D volume of cluster
    plt.figure(4)
    plt.plot(x, mean_areas[initial_plot_index:final_plot_index+1])
    plt.xlim(initial_plotting_time,final_plotting_time)
    plt.ylabel("Number of cells")
    plt.xlabel("time (hours)")
    plt.savefig(basedir + saving_plot_loc + 'INV_Mean_volume_cluster_' + 'multi' + '.png', dpi=300, bbox_inches="tight")

    plt_num += 1
