import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img1 = mpimg.imread('K_cst_IC_10_t_1000.png')
img2 = mpimg.imread('K_cst_IC_100_t_1000.png')
img3 = mpimg.imread('K_cst_IC_100_t_1000.png')
img4 = mpimg.imread('K_mult_IC_10_t_1000.png')
img5 = mpimg.imread('K_mult_IC_100_t_100000_almost_steady_zoomed_out.png')
img6 = mpimg.imread('K_mult_IC_1000_t_100000_almost_steady_zoomed_out.png')
img7 = mpimg.imread('K_diff_IC_10_t_1000.png')
img8 = mpimg.imread('K_diff_IC_100_t_1000.png')
img9 = mpimg.imread('K_diff_IC_1000_t_1000.png')


cols = ['q = {}'.format(col) for col in ['IC 10', 'IC 100', 'IC 1000']]
rows = ['b = {}'.format(row) for row in ['K cst', 'K mult', 'K diff']]



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