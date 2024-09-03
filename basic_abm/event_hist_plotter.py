import numpy as np
import pandas as pd
from ast import literal_eval

import matplotlib.pyplot as plt

from itertools import chain

# These three parameters are needed for accessing data and saving to files
basedir = '/Users/Nathan/Documents/Oxford/DPhil/clusters/basic_abm'
start_time = 1
end_time = 48

'''
Lineage tracer traces each cluster in turn back in time using event to find contributing clusters

Input arguments:
start_time: Timepoint to be traced back to and plotted
end_time: Timepoint to trace from and plot cluster 
basedir,
exp_date,
well_loc,

Output:
Series of subplots of start_time and end_time 
for each cluster's lineage next to each other

'''

df_end_now_csv_name_list = basedir, '/csv_files/', 'less_clus_pipeline_df_t_', str(end_time), '00', '.csv'
df_end_now_csv_name_list_2  =''.join(df_end_now_csv_name_list)
df_end_now = pd.read_csv(df_end_now_csv_name_list_2)
cluster_tags = df_end_now["Tag number"].to_numpy().astype(int)




cols = ["Tag number", "Cluster size", "Cluster Centre x", "Cluster Centre y", 
        "Event", "Clusters in event", "Timestep", "Date", "Well ID"]

event_cols = ["Move", "Coagulation", "Move large", "Splitting", 
              "Move large and grow", "Possible Coagulation",
              "Edge Appearance type 1", "Appearance type 1",
              "Edge Appearance type 2", "Appearance type 2", 
              "Edge Appearance type 3", "Appearance type 3", "Appearance Error"]

event_cols_plot = ["Move", "Coag", "Move l", "Splitting", 
              "Move l & g", "Poss Coag",
              "Edge App 1", "App 1",
              "Edge App 2", "App 2", 
              "Edge App 3", "App 3", "App Error"]

# event_cols = ["Coagulation", "Move large", "Splitting", 
#               "Move large and grow", "Possible Coagulation",
#               "Edge Appearance type 1", "Appearance type 1",
#               "Edge Appearance type 2", "Appearance type 2", 
#               "Edge Appearance type 3", "Appearance type 3", "Appearance Error"]

# event_cols_plot = ["Coag", "Move l", "Splitting", 
#               "Move l & g", "Poss Coag",
#               "Edge App 1", "App 1",
#               "Edge App 2", "App 2", 
#               "Edge App 3", "App 3", "App Error"]

cluster_appear_sizes = []
number_event = np.zeros(len(event_cols))
for i in range(end_time, start_time - 1, -1) :
    print('i is', i)
    time_i = str(i)
    df_step_csv_name_list = basedir, '/csv_files/', 'less_clus_pipeline_df_t_', time_i, '00', '.csv'
    df_step_csv_name_list_2  =''.join(df_step_csv_name_list)
    df_step = pd.read_csv(df_step_csv_name_list_2)
    # cluster_2D_areas = df_clus_areas.to_numpy()

    # Problematic events
    df_appear_err = df_step.loc[df_step['Event'] == 'Appearance Error']
    df_appear_1 = df_step.loc[df_step['Event'] == 'Appearance type 1']
    df_appear_2 = df_step.loc[df_step['Event'] == 'Appearance type 2']
    df_appear_3 = df_step.loc[df_step['Event'] == 'Appearance type 3']
    df_split = df_step.loc[df_step['Event'] == 'Splitting']
    df_move_l_and_g = df_step.loc[df_step['Event'] == 'Move large and grow']
    sizes_to_add_0 = df_appear_err['Cluster size']
    sizes_to_add_1 = df_appear_1['Cluster size']
    sizes_to_add_2 = df_appear_2['Cluster size']
    sizes_to_add_3 = df_appear_3['Cluster size']
    sizes_to_add_4 = df_split['Cluster size']
    sizes_to_add_5 = df_move_l_and_g['Cluster size']
    sizes_to_add = list(chain(sizes_to_add_0,sizes_to_add_1,sizes_to_add_2,
                              sizes_to_add_3,sizes_to_add_4,sizes_to_add_5))
    cluster_appear_sizes = np.append(cluster_appear_sizes, sizes_to_add)



    for j in range(len(event_cols)):
        df_add = df_step.loc[df_step['Event'] == event_cols[j]]
        # df_appear = df_step.loc[df_step['Event'] == 'Splitting']
        number_events_adding = df_add.shape[0]
        number_event[j] += number_events_adding


if len(event_cols) == 13:
    number_good_events = number_event[0] + number_event[1] + number_event[2] +\
                         number_event[5] + number_event[6] + number_event[8] + number_event[10]
    
    number_total_events = sum(number_event)

    accuracy = 100*number_good_events/number_total_events
print('Number events is', number_event)
print('Coag events is', number_event[1])
print('Accuracy is', accuracy)

print('Cluster event selected sizes', cluster_appear_sizes)

plt.hist(cluster_appear_sizes)
plt.show()

plt.bar(event_cols_plot, number_event)
plt.show()




