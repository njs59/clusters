import csv
import numpy as np
import pandas as pd


basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_date = '2017-02-03_'
time_array = range(1,98)
# Rename single digit values with 0 eg 1 to 01 for consistency
time_list = [str(x).zfill(2) for x in time_array]
well_loc = 's11'

for i in range(len(time_list)):
    csv_name_list = basedir, 'csv_folder/', exp_date, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '.csv'
    csv_name_list_2  =''.join(csv_name_list)

    # with open(csv_name_list_2, 'r') as f:
    #     reader = csv.reader(f)
    #     data = list(reader, header=False)
    # # data_array = np.array(data)
    # data_array = np.array(data, dtype=int)

 
    # # using loadtxt()
    # arr = np.loadtxt(csv_name_list_2,
    #                 delimiter=",")
    # # display(arr)

    df = pd.read_csv(csv_name_list_2)

    arr = df.to_numpy() 

    print('Yay')