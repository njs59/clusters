import numpy as np
import pandas as pd

# These three parameters are needed for accessing data and saving to files
basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_type = 'In_vitro_homogeneous_data/'
exp_date = '2017-02-03'
# exp_date = '2017-03-16'

# well_loc = 's11'
# multi_loc = ['s11', 's12']
multi_loc = ['s09', 's10']
# multi_loc = ['s073','s074']
start_time = 50
end_time = 97
timestep = 1

ODE_out = np.zeros((100,end_time+1-start_time))
ODE_out_multi = np.zeros((100,end_time+1-start_time))
for k in range(len(multi_loc)):
    well_loc = multi_loc[k]
    for i in range(start_time, end_time + 1, timestep):

        cluster_areas = []
        cluster_number = []
        df_step_csv_name_list = basedir, exp_type, 'post_processing_output/' , exp_date, '/', well_loc, 't', str(i).zfill(2) , 'c2_post_processing', '.csv'
        df_step_csv_name_list_2  =''.join(df_step_csv_name_list)
        df_step = pd.read_csv(df_step_csv_name_list_2)


        cluster_areas_well_ID = df_step["Cluster size"]

        cluster_areas = np.append(cluster_areas, cluster_areas_well_ID)

        cluster_number = np.round(cluster_areas/189)
        bin = list(range(1,101))
        bin.append(200)
        hist_arr = np.histogram(cluster_number,bin)

        time_ODE_output = hist_arr[0]
        ODE_out[:,i-start_time] = time_ODE_output
        print('Total cell count', sum(cluster_number))
        print('Cluster number', cluster_number)
        # print('Output for ODE', hist_arr)

    ODE_out_multi += ODE_out


ODE_out_multi = ODE_out_multi/len(multi_loc)

# save array into csv file 
np.savetxt("homogeneous/s09_inference_input_multi_well_t_50.csv", ODE_out_multi,  
            delimiter = ",")
# ODE_out.tofile('s11_inference_input.csv', sep = ',')