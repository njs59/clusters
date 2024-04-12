import numpy as np
import pandas as pd
import random
import sys

import number_circle as num_cir

def initialise(cell_num, x_len, y_len, area):
    cols = ["ID", "Area", "Centre x", "Centre y"]
    cell_df = pd.DataFrame(columns=cols)
    next_ID = 1
    for i in range(cell_num):
        x_loc = random.randint(1, x_len)
        y_loc = random.randint(1, y_len)

        cell_df.loc[i] = [next_ID, area, x_loc, y_loc]

        next_ID += 1


    return cell_df, next_ID

def sweep(cell_df, x_len, y_len, next_ID):
    num_overlaps = 1
    while num_overlaps > 0:
        all_pts = np.empty((0,3))
        for i in range(cell_df.shape[0]):
            clus_ID = cell_df.iloc[i,0]
            area_clus = cell_df.iloc[i,1]
            x_cen = cell_df.iloc[i,2]
            y_cen = cell_df.iloc[i,3]
            out_list, needed_of_final = num_cir.order_segment(area_clus)
            print(out_list)
            print(needed_of_final)

            points = num_cir.get_pixels(x_cen,y_cen, out_list, needed_of_final, clus_ID)
            # points_old = list(gen_points(cell_df.iloc[i,2],cell_df.iloc[i,3],cell_df.iloc[i,1],cell_df.iloc[i,0]))
            for j in range(len(points)):
                all_pts = np.vstack([all_pts, points[j]])


        # Apply periodic BCs
        for k in range(all_pts.shape[0]):
            if all_pts[k,0] > x_len:
                all_pts[k,0] = all_pts[k,0] - x_len 
            if all_pts[k,1] > y_len:
                all_pts[k,1] = all_pts[k,1] - y_len
            if all_pts[k,0] <= 0:
                all_pts[k,0] = all_pts[k,0] + x_len 
            if all_pts[k,1] <= 0:
                all_pts[k,1] = all_pts[k,1] + y_len       

        # check_for_coag
        visual_arr = np.zeros((x_len,y_len))
        for l in range(all_pts.shape[0]):
            visual_arr[int(all_pts[l,0])-1,int(all_pts[l,1])-1] += 1

        overlap_locs = np.where(visual_arr > 1)
        num_overlaps = len(overlap_locs[0])
        # for m in range(num_overlaps):
            # Search all_pts for IDs
        if num_overlaps > 0:
            x_search = overlap_locs[0][0] + 1
            y_search = overlap_locs[1][0] + 1

            x_vals = all_pts[:,0]
            y_vals = all_pts[:,1]
            x_match = np.where(x_vals == x_search)
            y_match = np.where(y_vals == y_search)
            # What happens if we have one of the clusters that's split over BCs
            # Move it all to the "positive" side and then find the average
            coag_indexes = np.intersect1d(x_match,y_match)

            coag_IDs = [int(all_pts[coag_indexes[0],2]),int(all_pts[coag_indexes[1],2])]

            # Store coag IDs
            cell_df, next_ID = Coagulation_overlap(cell_df, coag_IDs, next_ID, x_len, y_len)

            # ? Add Coagulation for neighbours here

    print('Sweep complete')
    return cell_df


def move_clusters(cell_df):

    # Assume for now movement independent of size
    for i in range(cell_df.shape[0]):
        r1 = random.random()
        # 99% Chance to move
        if r1 > 0.01:
            # Move
            # Now select direction (left,up,right,down)
            x_cen = cell_df['Centre x'][i]
            y_cen = cell_df['Centre y'][i]

            r2 = random.random()
            if r2 < 0.25:
                x_cen, y_cen = move_left(x_cen, y_cen)
            elif r2 < 0.5:
                x_cen, y_cen = move_up(x_cen, y_cen)
            elif r2 < 0.75:
                x_cen, y_cen = move_right(x_cen, y_cen)
            else:
                x_cen, y_cen = move_down(x_cen, y_cen)

            cell_df['Centre x'][i] = x_cen
            cell_df['Centre y'][i] = y_cen

    return cell_df

def visualise_arr(cell_df, x_len, y_len):
    all_pts = np.empty((0,3))
    for i in range(cell_df.shape[0]):
        clus_ID = cell_df.iloc[i,0]
        area_clus = cell_df.iloc[i,1]
        x_cen = cell_df.iloc[i,2]
        y_cen = cell_df.iloc[i,3]
        out_list, needed_of_final = num_cir.order_segment(area_clus)
        points = num_cir.get_pixels(x_cen,y_cen, out_list, needed_of_final, clus_ID)
        # points = list(gen_points(cell_df.iloc[i,2],cell_df.iloc[i,3],cell_df.iloc[i,1],cell_df.iloc[i,0]))
        for j in range(len(points)):
            all_pts = np.vstack([all_pts, points[j]])


    # Apply periodic BCs
    for k in range(all_pts.shape[0]):
        if all_pts[k,0] > x_len:
            all_pts[k,0] = all_pts[k,0] - x_len 
        if all_pts[k,1] > y_len:
            all_pts[k,1] = all_pts[k,1] - y_len       

    # check_for_coag
    visual_arr = np.zeros((x_len,y_len))
    for l in range(all_pts.shape[0]):
        visual_arr[int(all_pts[l,0])-1,int(all_pts[l,1])-1] += 1

    return visual_arr

def move_right(x,y):
    return x+1, y

def move_down(x,y):
    return x,y-1

def move_left(x,y):
    return x-1,y

def move_up(x,y):
    return x,y+1

def gen_points(x_init, y_init, area, ID):
    moves = [move_left, move_up, move_right, move_down]
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

def Coagulation_overlap(cell_df, coag_IDs, next_available_tag, x_len, y_len):
    cols = ["ID", "Area", "Centre x", "Centre y"]
    coag_df = pd.DataFrame(columns=cols)
    for i in range(len(coag_IDs)):
        index_drop = cell_df.index[cell_df['ID'] == coag_IDs[i]][0]
        coag_df = pd.concat([coag_df, cell_df.loc[cell_df['ID'] == coag_IDs[i]]])
        cell_df = cell_df.drop(index_drop)
    # Add check if centres are on opposite sides of periodic BCs
    if len(coag_IDs) == 2:
        if abs(coag_df.iloc[0,2] - coag_df.iloc[1,2]) > x_len/2:
            # Move centre from left to out right
            if coag_df.iloc[0,2] < coag_df.iloc[1,2]:
                coag_df.iloc[0,2] = coag_df.iloc[0,2] + x_len
            else:
                coag_df.iloc[1,2] = coag_df.iloc[1,2] + x_len

        if abs(coag_df.iloc[0,3] - coag_df.iloc[1,3]) > y_len/2:
            # Move centre from low to outside high value
            if coag_df.iloc[0,3] < coag_df.iloc[1,3]:
                coag_df.iloc[0,3] = coag_df.iloc[0,3] + y_len
            else:
                coag_df.iloc[1,3] = coag_df.iloc[1,3] + y_len
    elif len(coag_IDs) > 2:
        print('Multi coag')
        sys.exit(0)
    print(coag_df)
    new_ID = next_available_tag
    next_available_tag += 1
    
    new_area = 0
    coag_all_pts = np.empty((0,3))
    for j in range(len(coag_IDs)):
        new_area += int(coag_df.iloc[j,1])
        clus_ID = coag_df.iloc[j,0]
        area_clus = coag_df.iloc[j,1]
        x_cen = coag_df.iloc[j,2]
        y_cen = coag_df.iloc[j,3]
        out_list, needed_of_final = num_cir.order_segment(area_clus)
        print(out_list)
        print(needed_of_final)

        coag_points = num_cir.get_pixels(x_cen,y_cen, out_list, needed_of_final, clus_ID)

        # coag_points = list(gen_points(coag_df.iloc[i,2],coag_df.iloc[i,3],coag_df.iloc[i,1],coag_df.iloc[i,0]))
        for j in range(len(coag_points)):
            coag_all_pts = np.vstack([coag_all_pts, coag_points[j]])

    # FInd average centre for new centre
            # If it crosses the BC that's fine because it's sorted in periodic BCs in visualise
            # It's possible to have 
    new_centre_x = round(sum(coag_all_pts[:,0])/coag_all_pts.shape[0])
    new_centre_y = round(sum(coag_all_pts[:,1])/coag_all_pts.shape[0])
    if new_centre_x > x_len:
        new_centre_x = new_centre_x - x_len
    if new_centre_y > y_len:
        new_centre_y = new_centre_y - y_len
    # cell_df.loc[len(cell_df.index)] = [new_ID, new_area, new_centre_x, new_centre_y]
    # create extension
    df_extended = pd.DataFrame(columns=cols)
    df_extended.loc[0] = [new_ID, new_area, new_centre_x, new_centre_y]

    # concatenate to original
    cell_df = pd.concat([cell_df, df_extended], ignore_index=True)

    return cell_df, next_available_tag