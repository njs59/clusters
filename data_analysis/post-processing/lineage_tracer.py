import numpy as np
import pandas as pd
from ast import literal_eval

import matplotlib.pyplot as plt


basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_date = '2017-02-03'
time_array = range(1,98)
num_times = len(time_array)
# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(2) for x in time_array]
well_loc = 's11'

cols = ["Tag number", "Cluster size", "Cluster Centre x", "Cluster Centre y", 
           "Event", "Clusters in event", "Timestep", "Date", "Well ID"]

# cluster_lineage = [56]
cluster_lineage = [125]

for i in range(97, 30, -1) :
    print('i is', i)
    time_i = str(i).zfill(2)
    df_step_csv_name_list = basedir, '0_post_processing_output/', exp_date, '_', well_loc, 't', time_i, 'c2_post_processing', '.csv'
    df_step_csv_name_list_2  =''.join(df_step_csv_name_list)
    df_step = pd.read_csv(df_step_csv_name_list_2)
    # cluster_2D_areas = df_clus_areas.to_numpy()
    for j in range(len(cluster_lineage)):
        row_interest = df_step.loc[df_step['Tag number'] == cluster_lineage[j]]
        if (row_interest['Event'] == 'Coagulation').any():
        # if (row_interest.iloc[:, [4]] == 'Coagulation').any() == True:
            locs = row_interest.iloc[:, [5]]
            str_locs = locs.iloc[0]['Clusters in event']
            list_locs = literal_eval(str_locs)
            arr_locs = np.array(list_locs)
            res = [item for item in arr_locs if item not in cluster_lineage]
            cluster_lineage = np.append(cluster_lineage, res)

print(cluster_lineage)

# Find locations of clusters at time 30
df_step_csv_name_list = basedir, '0_post_processing_output/', exp_date, '_', well_loc, 't', '31', 'c2_post_processing', '.csv'
df_step_csv_name_list_2  =''.join(df_step_csv_name_list)
df_step_interest = pd.read_csv(df_step_csv_name_list_2)

rows_of_interest = pd.DataFrame(columns=cols)
for k in range(len(cluster_lineage)):
    new_row_of_interest = df_step_interest.loc[df_step['Tag number'] == cluster_lineage[k]]

    # to append df2 at the end of df1 dataframe
    rows_of_interest = pd.concat([rows_of_interest, new_row_of_interest])


# Store centres in array
df1 = rows_of_interest[['Cluster Centre x', 'Cluster Centre y']]
centres_2D_lineage = df1.to_numpy()

# Read in array for given timestep

# Locate indexes of clusters, print
index_csv_name_list = basedir, 'csv_folder/', exp_date, '_sphere_timelapse_', well_loc, 't', '31', 'c2', '_indexed', '.csv'
index_csv_name_list_2  =''.join(index_csv_name_list)
df_slice = pd.read_csv(index_csv_name_list_2, header=None)
current_array = df_slice.to_numpy()

indexes_lineage = []
for p in range(centres_2D_lineage.shape[0]):
    index_of_interest = current_array[int(centres_2D_lineage[p,0]),int(centres_2D_lineage[p,1])]
    indexes_lineage = np.append(indexes_lineage, index_of_interest)

descendents_arr = []

for q in range(len(indexes_lineage)):
    descendents_locs = np.where(current_array == int(indexes_lineage[q]))
    single_descendent_arr = np.asarray(descendents_locs)

    if q == 0:
        descendents_arr = single_descendent_arr
    else:
        descendents_arr = np.append(descendents_arr, single_descendent_arr, axis=1)



print('Yay')

bool_descendents = np.zeros(current_array.shape)

for r in range(descendents_arr.shape[1]):
    bool_descendents[descendents_arr[0,r], descendents_arr[1,r]] = 1

plt.imshow(bool_descendents)
plt.show()