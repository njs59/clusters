import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import lineage_tracer_function as ltf
import cluster_tracker_function as ctf

basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_date = '2017-02-03'
well_loc = 's11'


ctf.cluster_tracker(37, 97, 5, 10, basedir, exp_date, well_loc)


ltf.lineage_tracer(51,97, basedir, exp_date, well_loc)


    


# def lineage_calc():
#     list_of_clus = 0
#     return list_of_clus