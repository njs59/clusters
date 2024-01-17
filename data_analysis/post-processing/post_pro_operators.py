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