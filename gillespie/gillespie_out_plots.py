import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

# Read in mean area of cluster
df_mean_areas = pd.read_csv("gill_out_time.csv", header=None)
mean_areas = df_mean_areas.to_numpy()

x = range(1,101)
y = mean_areas[-1,:]
plt.bar(x,y)
plt.xlabel('Cluster size')
plt.ylabel('Average number of clusters')
plt.show()
# plt.savefig("plots_to_gif/final_plot" + ".jpg")
# plt.clf()


    