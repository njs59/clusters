import numpy as np

x = np.arange(1000000, dtype=np.int32).reshape((-1,2))
bad = np.arange(0, 1000000, 2000, dtype=np.int32)

print(x.shape)
print(bad.shape)

cleared = np.delete(x, np.where(np.in1d(x[:,0], bad)), 0)
print(cleared.shape)


initial_cells_number = 4

array = np.full((initial_cells_number, 2), 1, dtype=int)

initial_sus = int(initial_cells_number/2)
print(initial_sus)
for i in range(initial_sus):
    array[i,-1] = 0

print(array)

array_new = np.append(array, [[1,1]], axis=0)

print('New', array_new)
