import numpy as np
import matplotlib.pyplot as plt
import math

import glob
import contextlib
from PIL import Image

def animate_plot(psi, t, simulation_max):
    n_max = np.max(psi)
    plots_number = simulation_max
    for i in range(0,plots_number+1,1):
        plots_step = math.floor(len(t)/plots_number)
        x = range(1,101)
        y = psi[i*plots_step,:]
        plt.bar(x,y)
        plt.ylim([0, n_max])
        if i < 10:
            print ("value" + str(0) + str(0) + str(i) + ".jpg")
            plt.savefig("plots_to_gif/value" + str(0) + str(0) + str(i) + ".jpg")
            plt.clf()
        elif 10 <= i < 100:
            print ("value" + str(0) + str(i) + ".jpg")
            plt.savefig("plots_to_gif/value" + str(0) + str(i) + ".jpg")
            plt.clf()
        elif 100 <= i < 110:
            print ("values" + str(i) + ".jpg")
            plt.savefig("plots_to_gif/values" + str(i) + ".jpg")
            plt.clf()
        else:
            print ("values" + str(i) + ".jpg")
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
            


def animate_plot_mass(psi, t, simulation_max):
    n_max = np.max(psi)
    plots_number = simulation_max
    for i in range(0,plots_number+1,1):
        plots_step = math.floor(len(t)/plots_number)
        x = range(1,101)
        y = psi[i*plots_step,:]
        for z in range(1,101):
            y[z-1] = z*y[z-1]
        plt.bar(x,y)
        plt.ylim([0, n_max])
        if i < 10:
            print ("mass_value" + str(0) + str(0) + str(i) + ".jpg")
            plt.savefig("plots_to_gif/mass_value" + str(0) + str(0) + str(i) + ".jpg")
            plt.clf()
        elif 10 <= i < 100:
            print ("mass_value" + str(0) + str(i) + ".jpg")
            plt.savefig("plots_to_gif/mass_value" + str(0) + str(i) + ".jpg")
            plt.clf()
        elif 100 <= i < 110:
            print ("mass_values" + str(i) + ".jpg")
            plt.savefig("plots_to_gif/mass_values" + str(i) + ".jpg")
            plt.clf()
        else:
            print ("mass_values" + str(i) + ".jpg")
            plt.savefig("plots_to_gif/mass_value" + str(i) + ".jpg")
            plt.clf()

        # filepaths
        fp_in = "plots_to_gif/mass_value*.jpg"
        fp_out = "plots_to_gif/clustersize_mass.gif"

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
