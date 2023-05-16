import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import glob
import contextlib
from PIL import Image

mat_contents_norms = scipy.io.loadmat('array_norms_0.01.mat',  mdict=None, appendmat=True)
mat_contents_t = scipy.io.loadmat('array_t_0.01.mat', mdict=None, appendmat=True)

n_array_1 = mat_contents_norms['derivative_l2_norm']
t_array_1 = mat_contents_t['t']
print(np.shape(n_array_1))
print(np.shape(t_array_1))
#t_array_1 = t_array_1[ : -1]
print(np.shape(t_array_1))

# t_array_short_1 = [i for i in t_array_1 if i <= 2]
# t_short_shape_1 = np.shape(t_array_short_1)
# print(t_short_shape_1)
# t_short_len_1 = t_short_shape_1[0]
# print('Length: ', t_short_len_1)
# n_array_short_1 = n_array_1[:t_short_len_1]


mat_contents_norms = scipy.io.loadmat('array_norms_0.001.mat',  mdict=None, appendmat=True)
mat_contents_t = scipy.io.loadmat('array_t_0.001.mat', mdict=None, appendmat=True)

n_array_2 = mat_contents_norms['derivative_l2_norm']
t_array_2 = mat_contents_t['t']
print(np.shape(n_array_2))
print(np.shape(t_array_2))
#t_array_2 = t_array_2[ : -1]
print(np.shape(t_array_2))

# t_array_short_2 = [i for i in t_array_2 if i <= 2]
# t_short_shape_2 = np.shape(t_array_short_2)
# print(t_short_shape_2)
# t_short_len_2 = t_short_shape_2[0]
# print('Length: ', t_short_len_2)
# n_array_short_2 = n_array_2[:t_short_len_2]



mat_contents_norms = scipy.io.loadmat('array_norms_0.0001.mat',  mdict=None, appendmat=True)
mat_contents_t = scipy.io.loadmat('array_t_0.0001.mat', mdict=None, appendmat=True)

n_array_3 = mat_contents_norms['derivative_l2_norm']
t_array_3 = mat_contents_t['t']
print(np.shape(n_array_3))
print(np.shape(t_array_3))
#t_array_3 = t_array_3[ : -1]
print(np.shape(t_array_3))

# t_array_short_3 = [i for i in t_array_3 if i <= 2]
# t_short_shape_3 = np.shape(t_array_short_3)
# print(t_short_shape_3)
# t_short_len_3 = t_short_shape_3[0]
# print('Length: ', t_short_len_3)
# n_array_short_3 = n_array_3[:t_short_len_3]


#t_array_3 = np.delete(t_array_3, range(100))
#n_array_3 = np.delete(n_array_3, range(100))
#del t_array_3[:100]
#del n_array_3[:100]
print(np.shape(t_array_3))
# print(t_array_3)
plt.plot(t_array_1, n_array_1)
plt.plot(t_array_2, n_array_2)
plt.plot(t_array_3, n_array_3)
plt.yscale('log')
plt.legend(['b = 0.01', 'b = 0.001', 'b=0.0001'])
plt.show()



img1 = mpimg.imread('coag_and_shed/b_0.1_q_0.1.png')
img2 = mpimg.imread('coag_and_shed/b_0.1_q_0.01.png')
img3 = mpimg.imread('coag_and_shed/b_0.1_q_0.001.png')
img4 = mpimg.imread('coag_and_shed/b_0.01_q_0.1.png')
img5 = mpimg.imread('coag_and_shed/b_0.01_q_0.01.png')
img6 = mpimg.imread('coag_and_shed/b_0.01_q_0.001.png')
img7 = mpimg.imread('coag_and_shed/b_0.001_q_0.1.png')
img8 = mpimg.imread('coag_and_shed/b_0.001_q_0.01.png')
img9 = mpimg.imread('coag_and_shed/b_0.001_q_0.001.png')

cols = ['q = {}'.format(col) for col in ['0.1', '0.01', '0.001']]
rows = ['b = {}'.format(row) for row in ['0.1', '0.01', '0.001']]



fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 8))

for ax, col in zip(axes[0], cols):
    ax.set_title(col)

for ax, row in zip(axes[:,0], rows):
    ax.set_ylabel(row, rotation=90, size='large')


plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
plt.tight_layout()
plt.subplot(3,3,1)
plt.imshow(img1)

plt.subplot(3,3,2)
plt.imshow(img2)

plt.subplot(3,3,3)
plt.imshow(img3)

plt.subplot(3,3,4)
plt.imshow(img4)

plt.subplot(3,3,5)
plt.imshow(img5)

plt.subplot(3,3,6)
plt.imshow(img6)

plt.subplot(3,3,7)
plt.imshow(img7)

plt.subplot(3,3,8)
plt.imshow(img8)

plt.subplot(3,3,9)
plt.imshow(img9)
plt.show()

#####################


img1 = mpimg.imread('coag_and_shed/b_0.1_q_0.1_zoomed.png')
img2 = mpimg.imread('coag_and_shed/b_0.1_q_0.01_zoomed.png')
img3 = mpimg.imread('coag_and_shed/b_0.1_q_0.001_zoomed.png')
img4 = mpimg.imread('coag_and_shed/b_0.01_q_0.1_zoomed.png')
img5 = mpimg.imread('coag_and_shed/b_0.01_q_0.01_zoomed.png')
img6 = mpimg.imread('coag_and_shed/b_0.01_q_0.001_zoomed.png')
img7 = mpimg.imread('coag_and_shed/b_0.001_q_0.1_zoomed.png')
img8 = mpimg.imread('coag_and_shed/b_0.001_q_0.01_zoomed.png')
img9 = mpimg.imread('coag_and_shed/b_0.001_q_0.001_zoomed.png')

cols = ['q = {}'.format(col) for col in ['0.1', '0.01', '0.001']]
rows = ['b = {}'.format(row) for row in ['0.1', '0.01', '0.001']]



fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 8))

for ax, col in zip(axes[0], cols):
    ax.set_title(col)

for ax, row in zip(axes[:,0], rows):
    ax.set_ylabel(row, rotation=90, size='large')


plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
plt.tight_layout()
plt.subplot(3,3,1)
plt.imshow(img1)

plt.subplot(3,3,2)
plt.imshow(img2)

plt.subplot(3,3,3)
plt.imshow(img3)

plt.subplot(3,3,4)
plt.imshow(img4)

plt.subplot(3,3,5)
plt.imshow(img5)

plt.subplot(3,3,6)
plt.imshow(img6)

plt.subplot(3,3,7)
plt.imshow(img7)

plt.subplot(3,3,8)
plt.imshow(img8)

plt.subplot(3,3,9)
plt.imshow(img9)
plt.show()




