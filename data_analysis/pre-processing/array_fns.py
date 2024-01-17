import numpy as np

def update_arr(arr):
    global arr_2, arr_3
    index = np.where(arr_2 == arr)
    if len(index[0]) != 0:        
        i = arr_3[index[0]][0]
    else:
        i = 0
    return i

arr_1 = np.array([[1,2],[3,4]])
arr_2 = np.array([1,3,12,16])
arr_3 = np.array([13,19,20,21])

applyall = np.vectorize(update_arr)
res = applyall(arr_1)
print(res)

