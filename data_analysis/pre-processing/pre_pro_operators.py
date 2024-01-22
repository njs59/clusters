import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def threshold_arr(tf_array, threshold):
    tf_ad = tf_array
    for p in range(tf_array.shape[0]):
      for q in range(tf_array.shape[1]):
        for r in range(tf_array.shape[2]):
            if tf_array[(p,q,r)] > threshold:
                tf_ad[(p,q,r)] = 1
            else:
                tf_ad[(p,q,r)] = 0

    # tf_array_bool = np.array(tf_ad, dtype = bool)
    tf_array_bool = tf_ad

    # reshaping the array from 3D
    # matrix to 2D matrix.
    arr_reshaped = tf_array_bool.reshape(tf_array_bool.shape[0], -1)
 
    # saving reshaped array to file.
    np.savetxt("/Users/Nathan/Documents/Oxford/DPhil/test_3D.txt", arr_reshaped)
 
    # retrieving data from file.
    loaded_arr = np.loadtxt("/Users/Nathan/Documents/Oxford/DPhil/test_3D.txt")
 
    load_original_arr = loaded_arr.reshape(
        loaded_arr.shape[0], loaded_arr.shape[1] // tf_array_bool.shape[2], tf_array_bool.shape[2])
    
    # check the shapes:
    print("shape of arr: ", tf_array_bool.shape)
    print("shape of load_original_arr: ", load_original_arr.shape)
    
    # check if both arrays are same or not:
    if (load_original_arr == tf_array_bool).all():
        print("Yes, both the arrays are same")
    else:
        print("No, both the arrays are not same")


    return tf_array_bool


def remove_fragments(area, num_clus, min_clus_size):
    ## Get a list of indexes for slice of array that correspond to large enough to be considered a cluster

    index_to_del = np.argwhere(area < min_clus_size)
    area_new = np.delete(area, index_to_del)

    # print(lw)
    # print(area_new)


    # print(index_to_del)

    index_keep = np.arange(num_clus+1)
    for i in range(len(index_to_del)):
        index_keep = np.delete(index_keep, np.where(index_keep == index_to_del[i]))

    # print(index_keep)

    return area_new, index_keep

def save_clus_areas(i, area_new, cluster_areas):
    if i == 0:
      cluster_areas = np.append(cluster_areas, area_new, axis=0)


    elif i == 1:
      print('Compare', len(area_new), cluster_areas.shape[0])
      if len(area_new) < cluster_areas.shape[0]:
        area_to_add = np.zeros((1,cluster_areas.shape[0]))

        for n in range(len(area_new)):
          area_to_add[0,n] = area_new[n]
        cluster_areas = np.vstack((cluster_areas, area_to_add))
      else:
        ## Add zeros to current array
        extra_clusters = len(area_new) - cluster_areas.shape[0]
        for v in range(extra_clusters):
          cluster_areas = np.append(cluster_areas,0)
        # # Now add the new data
        area_to_add = np.zeros((1,cluster_areas.shape[0]))
        for n in range(len(area_new)):
          area_to_add[0,n] = area_new[n]
        cluster_areas = np.vstack((cluster_areas, area_to_add))
      print('Shape clus', cluster_areas.shape)

    else:
      print('Compare', len(area_new), cluster_areas.shape[1])
      if len(area_new) < cluster_areas.shape[1]:
        area_to_add = np.zeros((1,cluster_areas.shape[1]))
        for n in range(len(area_new)):
          area_to_add[0,n] = area_new[n]
        cluster_areas = np.vstack((cluster_areas, area_to_add))
      else:
        ## Add zeros to current array
        extra_clusters = len(area_new) - cluster_areas.shape[1]
        extra_zeros = np.zeros((cluster_areas.shape[0], extra_clusters))
        print('Extras', extra_clusters, cluster_areas.shape)
        print('Shapes', extra_zeros.shape)
        cluster_areas = np.hstack((cluster_areas, extra_zeros))
        # Now add the new data
        area_to_add = np.zeros((1,cluster_areas.shape[1]))
        for n in range(len(area_new)):
          area_to_add[0,n] = area_new[n]
        cluster_areas = np.vstack((cluster_areas, area_to_add))
      print('Shape clus', cluster_areas.shape)

    return cluster_areas


def update_hist(num, data):
    plt.cla()
    plt.gca()
    # plt.set_ylim([0,60])
    plt.axis([150,25000,0,200])
    plt.hist(data[num,:], bins=[200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000])



def update_heat_map(data):
  my_cmap = mpl.colormaps['spring']
  my_cmap.set_under('k')
  plt.imshow(data, cmap=my_cmap, vmin = 1)
  plt.axis([0, data.shape[1], 0, data.shape[0]])
  plt.colorbar()
  plt.show()

