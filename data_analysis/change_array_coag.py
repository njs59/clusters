import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.ndimage import *
from skimage import measure
from pylab import arange

import calc_centres as cc

## These are outputs of the basic abm with 0.5 prob_move and 0 prob_prolif

list_1s = [[3, 1],[9, 0],[10,  4],[9, 5],[1, 1],[9, 7],[3, 9],[7, 1],[2, 8],[4, 2],[7, 8],[3, 8]]

print([3,1] in list_1s)

arr_1 = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        if [i+1,j+1] in list_1s:
            arr_1[i,j] = 1

print(arr_1)


list_2s = [[2, 8],[10, 4],[3, 9],[3, 8],[7, 8],[9, 7],[3, 1],[10, 5],[2, 1],[7, 1],[4, 1],[9, 0]]

arr_2 = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        if [i+1,j+1] in list_2s:
            arr_2[i,j] = 1

print(arr_2)


# plt.imshow(arr_1, interpolation='none')
# plt.colorbar()
# plt.show()

# plt.imshow(arr_2, interpolation='none')
# plt.colorbar()
# plt.show()

diff_arr = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        diff_arr[i,j] = arr_2[i,j] - arr_1[i,j]

# plt.imshow(arr_1, interpolation='none')
# plt.colorbar()
# plt.show()

# plt.imshow(arr_2, interpolation='none')
# plt.colorbar()
# plt.show()

# plt.imshow(diff_arr, interpolation='none')
# plt.colorbar()
# plt.show()


labeled_array, num_features = label(arr_1)

print(labeled_array)
print(num_features)

area = sum(arr_1, labeled_array, index=arange(labeled_array.max() + 1))
areaImg = area[labeled_array]

#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
##################################        KEY CODE BELOW     ##########################################
#######################################################################################################
#######################################################################################################
#######################################################################################################




###################### timepoints_3D_array code below  ########################
print(arr_1.shape)
labeled_1, num_1 = label(arr_1[:, :])
props_1 = measure.regionprops_table(
        labeled_1, properties=('label', 'area', 'bbox'))
props_1_df = pd.DataFrame(props_1)
props_1_df = props_1_df.sort_values('area', ascending=False)
# Show top five rows
print(props_1_df.shape)
# props_0_df.head()
print(props_1_df)


##threshold size for cluster
threshold = 0
indexes_1 = np.argwhere(area < threshold)
# print(indexes_1)
# index_to_del_1 = np.concatenate( indexes_1, axis=0 )
index_to_del_1 = []
index_keep_1 = np.arange(num_1+1)
for i in range(len(index_to_del_1)):
  index_keep_1 = np.delete(index_keep_1, np.where(index_keep_1 == index_to_del_1[i]))

######################################

print(arr_2.shape)
labeled_2, num_2 = label(arr_2[:, :])
props_2 = measure.regionprops_table(
        labeled_2, properties=('label', 'area', 'bbox'))
props_2_df = pd.DataFrame(props_2)
props_2_df = props_2_df.sort_values('area', ascending=False)
# Show top five rows
print(props_2_df.shape)
# props_0_df.head()
print(props_2_df)


##threshold size for cluster
indexes_2 = np.argwhere(area < threshold)
# print(indexes_2)
# index_to_del_2 = np.concatenate( indexes_2, axis=0 )
index_to_del_2 = []
index_keep_2 = np.arange(num_2+1)
for i in range(len(index_to_del_2)):
  index_keep_2 = np.delete(index_keep_2, np.where(index_keep_2 == index_to_del_2[i]))



###################### Calculate centres of clusters ##############################
centres_1 = cc.calc_clus_centre(labeled_1, index_keep_1)
centres_2 = cc.calc_clus_centre(labeled_2, index_keep_2)

print(centres_1)





################### Calculate how many centres were in previous timestep locs ##########

## USe this value as an example, will need to loop over all index values
d = np.argwhere(labeled_2 == index_keep_2[2])

#print(d)
#print(centres_2D_old)
print(d.shape)
for l in range(len(index_keep_2)):
    same_locs = 0
    same_locs_store = np.array([])
    d = np.argwhere(labeled_2 == index_keep_2[l])
    for m in range(d.shape[0]):
       for n in range(centres_1.shape[0]):
        # Time 1 is old timestep in this case
        if d[m,0] == centres_1[n,0] and d[m,1] == centres_1[n,1]:
            same_locs += 1
            if same_locs == 1:
                same_locs_store = np.append(same_locs_store, d[m,:])
            else:
                same_locs_store = np.vstack([same_locs_store, d[m,:]])
    print(same_locs)
    print(same_locs_store)

# Figure out how to save multiple of same_locs and same_locs_store   

