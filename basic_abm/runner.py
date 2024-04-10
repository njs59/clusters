import numpy as np
import pandas as pd

import functions as fns

x_len = 10
y_len = 10
next_available_ID = 1

cols = ["ID", "Radius", "Centre x", "Centre y"]
cell_df = pd.DataFrame(columns=cols)



initial_df = fns.initialise(10,x_len,y_len,2)

cell_df = fns.sweep(initial_df, x_len, y_len)

print(initial_df)
