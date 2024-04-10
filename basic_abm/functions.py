import numpy as np
import pandas as pd
import random

def initialise(cell_num, x_len, y_len, area):
    cols = ["ID", "Area", "Centre x", "Centre y"]
    cell_df = pd.DataFrame(columns=cols)
    next_ID = 1
    for i in range(cell_num):
        x_loc = random.randint(1, x_len)
        y_loc = random.randint(1, y_len)

        cell_df.loc[i] = [next_ID, area, x_loc, y_loc]

        next_ID += 1


    return cell_df

def sweep(cell_df, x_len, y_len):
    print('Hit')
    all_pts = np.empty((0,3))
    for i in range(cell_df.shape[0]):
        points = list(gen_points(cell_df.iloc[i,2],cell_df.iloc[i,3],cell_df.iloc[i,1],cell_df.iloc[i,0]))
        for j in range(len(points)):
            all_pts = np.vstack([all_pts, points[j]])

    print('Hit 2')

    # Apply periodic BCs
    for k in range(all_pts.shape[0]):
        if all_pts[k,1] > x_len:
            all_pts[k,1] = all_pts[k,1] - x_len 
        if all_pts[k,2] > y_len:
            all_pts[k,2] = all_pts[k,2] - y_len       

    # check_for_coag
    visual_arr = np.zeros((x_len,y_len))
    for l in range(all_pts.shape[0]):
        visual_arr[int(all_pts[l,1])-1,int(all_pts[l,2])-1] += 1

    overlap_locs = np.where(visual_arr > 1)
    num_overlaps = len(overlap_locs[0])
    for m in range(num_overlaps):
        # Search all_pts for IDs
        x_search = overlap_locs[0][m] + 1
        y_search = overlap_locs[1][m] + 1

        x_vals = all_pts[:,1]
        y_vals = all_pts[:,2]
        x_match = np.where(x_vals == x_search)
        y_match = np.where(y_vals == y_search)

        res = []
        p = 0
        while (p < len(x_match)):
            if (y_match.count(x_match[p]) > 0):
                res.append(x_match[p])
            p += 1



    print('Hit 3')



    # Move
    return cell_df

def move_right(x,y):
    return x+1, y

def move_down(x,y):
    return x,y-1

def move_left(x,y):
    return x-1,y

def move_up(x,y):
    return x,y+1

def gen_points(x_init, y_init, area, ID):
    moves = [move_right, move_down, move_left, move_up]
    from itertools import cycle
    _moves = cycle(moves)
    n = ID
    pos = x_init,y_init
    pos_x = x_init
    pos_y = y_init
    times_to_move = 1
    ticker = 1

    yield [n,pos_x,pos_y]

    while True:
        for _ in range(2):
            move = next(_moves)
            for _ in range(times_to_move):
                if ticker >= area:
                    return
                pos = move(*pos)
                pos_x = pos[0]
                pos_y = pos[1]
                ticker += 1
                yield [n,pos_x,pos_y]

        times_to_move+=1

def periodic_BCs():
    return 0


def Brownian_Move():
    return 0

def Coagulation():
    return 0