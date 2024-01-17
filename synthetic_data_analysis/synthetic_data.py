import matplotlib.pylab as plt
import numpy as np
import random



from scipy.ndimage import *
from pylab import arange


np.random.seed(0)

arr = np.random.random((10,10))

tf_arr = arr
for p in range(10):
    for q in range(10):
        if arr[(p,q)] > 0.7:
            tf_arr[(p,q)] = 1
        else:
            tf_arr[(p,q)] = 0
print(arr)


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.label.html
# It doesn't give an algorithm but mark_for_merge and label_line_with_neighbor make it look
# like it iterates over a bunch of different lines/regions/blocks by stride and labels each group in that region. 
# It merges labels between regions using a union-find/disjoint-set.
labeled_array, num_features = label(tf_arr)

print(labeled_array)
print(num_features)

area = measurements.sum(tf_arr, labeled_array, index=arange(labeled_array.max() + 1))
areaImg = area[labeled_array]



plt.imshow(tf_arr, interpolation='none')
plt.colorbar()
plt.show()


plt.imshow(labeled_array, interpolation='none')
plt.colorbar()
plt.show()

plt.imshow(areaImg, origin='lower')
plt.colorbar()
plt.title("Clusters by area")
plt.show()