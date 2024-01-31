import math
import numpy as np

## Calculate centres of mass from arrays
def calc_clus_centre(labelled_arr):
## Returns a list of centres of clusters with desired indexes from a labelled array
    centres = np.array([])
    for i in range(1,labelled_arr.max()+1):
        locs_of_size = np.transpose((labelled_arr==i).nonzero())
        centre_of_mass = locs_of_size.mean(axis=0)
        centre_of_mass = np.rint(centre_of_mass)
        centres = np.append(centres, centre_of_mass)

    centres_2D = np.reshape(centres, (-1, 2))
    return centres_2D


def previous_clusters_at_loc(labelled_arr, centres_old, comparison_index):

    same_locs = 0
    same_locs_store = np.array([])

    d = np.argwhere(labelled_arr == comparison_index)
    for m in range(d.shape[0]):
        for n in range(centres_old.shape[0]):
        # Time 1 is old timestep in this case
            if d[m,0] == centres_old[n,0] and d[m,1] == centres_old[n,1]:
                same_locs += 1
                if same_locs == 1:
                    same_locs_store = np.append(same_locs_store, d[m,:])
                else:
                    same_locs_store = np.vstack([same_locs_store, d[m,:]])
    # print(same_locs)
    # print(same_locs_store)

    return same_locs, same_locs_store


def nearby_clusters(x_loc, y_loc, search_radius, labelled_arr):
    search_arr = labelled_arr[x_loc - search_radius : x_loc + search_radius,
                              y_loc - search_radius: y_loc + search_radius]
    # search_arr[search_arr == index] = 0
    clusters_index_present = np.unique(search_arr)
    #Remove 0's from consideration
    clusters_index_output = clusters_index_present[1:]

    distances = []
    for i in range(1,len(clusters_index_present)):
        # if len(clusters_index_present) > 2:
        #     print('Hello')
        # Looping this way ignores the 0's present

        list_of_locs = np.where(search_arr == clusters_index_present[i])
        for k in range(len(list_of_locs[0])):
            min_dist = math.inf
            # Loop over each element of cluster visible
            dist_x = abs(list_of_locs[0][k] - search_radius)
            dist_y = abs(list_of_locs[1][k] - search_radius)

            dist = dist_x + dist_y + 1
            min_dist = min(min_dist, dist)

        distances = np.append(distances, min_dist)

    return clusters_index_output, distances


def pick_cluster_inverse_dist(clusters_index_output, distances):
    if 0 in distances:
        position = np.where(distances == 0)
        return clusters_index_output[position]
    else:
        weights = np.reciprocal(distances)     # Invert all distances
        weights = weights / np.sum(weights)         # Normalize
        cluster_selected = np.random.choice(clusters_index_output, p=weights) # Sample
        return cluster_selected

# def calc_clus_centre(labelled_arr, index_keep):
# ## Returns a list of centres of clusters with desired indexes from a labelled array
#     centres = np.array([])
#     for i in range(len(index_keep)):
#         locs_of_size = np.transpose((labelled_arr==index_keep[i]).nonzero())
#         centre_of_mass = locs_of_size.mean(axis=0)
#         centre_of_mass = np.rint(centre_of_mass)
#         centres = np.append(centres, centre_of_mass)

#     centres_2D = np.reshape(centres, (-1, 2))
#     return centres_2D