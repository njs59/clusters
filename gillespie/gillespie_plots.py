import numpy as np
import matplotlib.pyplot as plt

import glob
import contextlib
from PIL import Image

def animate_plot(psi, t):
    n_max = np.max(psi)
    for i in range(0,len(t),1):
        x = range(1,101)
        y = psi[i,:]
        plt.bar(x,y)
        plt.ylim([0, n_max])
        if i < 10:
            print ("value" + str(0) + str(i) + ".jpg")
            plt.savefig("plots_to_gif/value" + str(0) + str(i) + ".jpg")
            plt.clf()
        elif i == 100:
            print ("values" + str(i) + ".jpg")
            plt.savefig("plots_to_gif/values" + str(i) + ".jpg")
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
