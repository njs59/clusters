import lineage_tracer_function as ltf
import cluster_tracker_function as ctf

# These three parameters are needed for accessing data and saving to files
basedir = '/Users/Nathan/Documents/Oxford/DPhil/'
exp_date = '2017-02-03'
well_loc = 's11'

'''
Cluster tracker tracks an individually taggged cluster over time
Input arguments: 
    start_time, first timepoint to plot
    end_time, final timepoint to plot
    timejump, number of timesteps between each plot
    cluster_index_final_time, row in final time to select cluster ID tag from
    basedir,
    exp_date
    well_loc

Output:
    Series of plots 
'''
ctf.cluster_tracker(37, 97, 5, 10, basedir, exp_date, well_loc)



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
ltf.lineage_tracer(51,97, basedir, exp_date, well_loc)
