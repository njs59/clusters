import matplotlib.pyplot as plt
import numpy as np

## These are outputs of the basic abm with 0.5 prob_move and 0 prob_prolif

list_1s = [[3, 1],[9, 0],[10,  4],[9, 5],[1, 1],[9, 7],[3, 9],[7, 1],[2, 8],[4, 2],[7, 8],[3, 8]]

print([3,1] in list_1s)

arr_1 = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        if [i+1,j+1] in list_1s:
            arr_1[i,j] = 1

print(arr_1)


list_2s = [[2, 8],[10, 4],[3, 9],[3, 8],[7, 8],[9, 7],[3, 1],[10, 5],[2, 1],[7, 1],[4, 1],[9, 0]]

arr_2 = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        if [i+1,j+1] in list_2s:
            arr_2[i,j] = 1

print(arr_2)


# plt.imshow(arr_1, interpolation='none')
# plt.colorbar()
# plt.show()

# plt.imshow(arr_2, interpolation='none')
# plt.colorbar()
# plt.show()

diff_arr = np.zeros((10,10))

for i in range(10):
    for j in range(10):
        diff_arr[i,j] = arr_2[i,j] - arr_1[i,j]

plt.imshow(diff_arr, interpolation='none')
plt.colorbar()
plt.show()