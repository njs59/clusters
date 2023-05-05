import scipy.io
import numpy as np
import matplotlib.pyplot as plt

import glob
import contextlib
from PIL import Image

mat_contents_n = scipy.io.loadmat('array_n.mat',  mdict=None, appendmat=True)
mat_contents_t = scipy.io.loadmat('array_t.mat', mdict=None, appendmat=True)

n_array = mat_contents_n['n']
t_array = mat_contents_t['t']

print(t_array)
print(np.shape(n_array))
print(np.shape(t_array))
print(n_array)

x = t_array[:,0]
# y =  n_array[:,2]
# print(x)
# print(y)
# print(len(x))
# print(len(y))
n_max = np.max(n_array)

for i in range(0,100,1):
    y = n_array[:,i]
    plt.plot(x,y)
    plt.ylim([0, n_max])
    if i < 10:
        print ("value" + str(0) + str(i) + ".jpg")
        plt.savefig("plots_to_gif/value" + str(0) + str(i) + ".jpg")
        plt.clf()
    else:
        print ("value" + str(i) + ".jpg")
        plt.savefig("plots_to_gif/value" + str(i) + ".jpg")
        plt.clf()


# filepaths
fp_in = "plots_to_gif/value*.jpg"
fp_out = "plots_to_gif/clustersize.gif"

# use exit stack to automatically close opened images
with contextlib.ExitStack() as stack:

    # lazily load images
    imgs = (stack.enter_context(Image.open(f))
            for f in sorted(glob.glob(fp_in)))

    # extract  first image from iterator
    img = next(imgs)

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=200, loop=0)
