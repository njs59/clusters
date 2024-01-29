import matplotlib.pyplot as plt
import numpy as np
import random

random.seed(123)

dim = 10

arr = np.zeros((dim,dim))

arr[1,1] = 1
arr[4,4] = 1
arr[8,8] = 1

cells = np.nonzero(arr)
print(cells)
timesteps = 9

for j in range(timesteps):
    cells = np.where(arr > 0)
    selected_item = random.choice(range(len(cells[0])))

    x = cells[0][selected_item]
    y = cells[1][selected_item]

    direction = random.choice(range(4))

    if direction == 0:
        # North
        success = 0
        while success == 0:
            y += 1
            if y >= dim:
                print('Tried to expand outside area N')
                success = 1
            elif arr[x,y] == 0:
                success = 1
                arr[x,y] = 1
            else:
                print('Moving target')

    if direction == 1:
        # East
        success = 0
        while success == 0:
            x += 1
            if x >= dim:
                print('Tried to expand outside area E')
                success = 1
            elif arr[x,y] == 0:
                success = 1
                arr[x,y] = 1
            else:
                print('Moving target')

    if direction == 2:
        # South
        success = 0
        while success == 0:
            y -= 1
            if y < 0:
                print('Tried to expand outside area S')
                success = 1
            elif arr[x,y] == 0:
                success = 1
                arr[x,y] = 1
            else:
                print('Moving target')

    if direction == 3:
        # West
        success = 0
        while success == 0:
            x -= 1
            if x < 0:
                print('Tried to expand outside area W')
                success = 1
            elif arr[x,y] == 0:
                success = 1
                arr[x,y] = 1
            else:
                print('Moving target')

print('Array', arr)
plt.imshow(arr)
plt.show()