import csv
import numpy as np

with open('data2.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))



data_array = np.array(data)
data_array = np.delete(data_array, 0, 0)

# for i in range(1,data_array.shape[0]):
#         data_array[i,1] = int(data_array[i,1])

data_2 = [list( map(int,i) ) for i in data_array]

print(data_array)
