import numpy as np

def initial_setup(initial_cells_number, initial_pro_prop):
    init_array = np.full((initial_cells_number, 2), 1, dtype=int)

    initial_pro = int(initial_pro_prop * initial_cells_number)
    # print(initial_pro)
    for i in range(initial_pro):
        init_array[i,-1] = 0

    return init_array
