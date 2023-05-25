import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img1 = mpimg.imread('K_cst_IC_10_N_10.png')
img2 = mpimg.imread('K_cst_IC_10_N_100.png')
img3 = mpimg.imread('K_cst_IC_50_N_50.png')
img4 = mpimg.imread('K_cst_IC_50_N_100.png')
img5 = mpimg.imread('K_cst_IC_100_N_50.png')
img6 = mpimg.imread('K_cst_IC_100_N_100.png')
img7 = mpimg.imread('K_cst_IC_1000_N_100.png')
img8 = mpimg.imread('K_cst_IC_1000_N_1000.png')


#cols = ['q = {}'.format(col) for col in ['0.1', '0.01', '0.001']]
rows = ['IC = {}'.format(row) for row in ['10', '50', '100', '1000']]



fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 8))

# for ax, col in zip(axes[0], cols):
#     ax.set_title(col)

for ax, row in zip(axes[:,0], rows):
    ax.set_ylabel(row, rotation=90, size='large')


#plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
#plt.tight_layout()
plt.subplot(4,2,1)
plt.imshow(img1)

plt.subplot(4,2,2)
plt.imshow(img2)

plt.subplot(4,2,3)
plt.imshow(img3)

plt.subplot(4,2,4)
plt.imshow(img4)

plt.subplot(4,2,5)
plt.imshow(img5)

plt.subplot(4,2,6)
plt.imshow(img6)

plt.subplot(4,2,7)
plt.imshow(img7)

plt.subplot(4,2,8)
plt.imshow(img8)

# plt.subplot(3,3,9)
# plt.imshow(img9)
plt.show()