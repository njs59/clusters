import numpy as np
import matplotlib.pyplot as plt
import math
import scipy as sci

import glob
import contextlib
from PIL import Image


def final_step_plot(psi, t, simulation_max):
    n_max = np.max(psi)
    # plots_number = simulation_max
    x = range(1,101)
    y = psi[-1,:]
    plt.bar(x,y)
    plt.xlabel('Cluster size')
    plt.ylabel('Average number of clusters')
    plt.show()
    # plt.savefig("plots_to_gif/final_plot" + ".jpg")
    plt.clf()

def final_step_normalise_plot(psi, t, simulation_max):
    n_max = np.max(psi)
    # plots_number = simulation_max
    x = range(1,101)
    y_raw = psi[-1,:]
    y_sum = np.sum(y_raw)
    y = y_raw/y_sum
    y_check = np.sum(y)
    print('Check', y_check)
    plt.bar(x,y)
    plt.xlabel('Cluster size')
    plt.ylabel('Normalised number of clusters')
    plt.savefig("plots_to_gif/final_plot_normalised" + ".jpg")
    plt.clf()            

def final_step_mass_plot(psi, t, simulation_max):
    n_max = np.max(psi)
    # plots_number = simulation_max
    x = range(1,101)
    y_raw = psi[-1,:]
    y_mass = np.zeros(100)
    for i in range(100):
        y_mass[i] = (i+1)*y_raw[i]
    y_sum = np.sum(y_mass)
    y = y_mass/y_sum
    y_check = np.sum(y)
    print('Check', y_check)
    plt.bar(x,y)
    plt.xlabel('Cluster size')
    plt.ylabel('Chance cell is in cluster')
    # plt.savefig("plots_to_gif/final_plot_mass" + ".jpg")
    plt.savefig("final_plot_mass" + ".jpg")
    plt.clf()   

def final_step_mass_hist(psi, t, simulation_max, sim_num):
    n_max = np.max(psi)
    # plots_number = simulation_max
    x = range(1,101,5)
    y_raw = psi[-1,:]
    print('y raw', y_raw)
    y_raw_scale = sim_num*y_raw
    hist_values = []
    for k in range (100):
        count = y_raw_scale[k]
        count_round = round(count)
        for l in range(count_round*(k+1)):
            hist_values.append(k+1)
            #print('l', l)

    #y_mass = np.zeros(20)
    #for j in range(20):
    #    for i in range(5):
    #        y_mass[j] = (5*j+i+1)*y_raw[5*j+i]
    #y_sum = np.sum(y_mass)
    #y = y_mass/y_sum
    #y_check = np.sum(y)
    #print('Check', y_check)
    print('Hist values', hist_values)
    plt.hist(hist_values, bins=20, density=True)
    #plt.bar(x,y)
    plt.xlabel('Cluster size')
    plt.ylabel('Chance cell is in cluster')
    plt.savefig("plots_to_gif/final_plot_mass_hist" + ".jpg")
    iqr = sci.stats.iqr(hist_values)
    print('iqr', iqr)
    plt.clf()  


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
            print ("value" + str(i) + ".jpg")
            plt.savefig("plots_to_gif/value" + str(i) + ".jpg")
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
            plt.savefig("plots_to_gif/mass_values" + str(i) + ".jpg")
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
