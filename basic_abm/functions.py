import math
import numpy as np
import pandas as pd
import random
import sys

import number_circle as num_cir

def initialise(cell_num, x_len, y_len, area):
    cols = ["ID", "Area", "Centre x", "Centre y", "Radius"]
    cell_df = pd.DataFrame(columns=cols)
    next_ID = 1
    for i in range(cell_num):
        x_loc = random.randint(1, x_len)
        y_loc = random.randint(1, y_len)

        out_list, needed_of_final, radius = num_cir.order_segment(area)

        cell_df.loc[i] = [next_ID, area, x_loc, y_loc, radius]

        next_ID += 1


    return cell_df, next_ID

def sweep(cell_df, x_len, y_len, next_ID):
    # num_overlaps = 1
    # while num_overlaps > 0:
    # all_pts = np.empty((0,3))
    cols = ["ID", "Area", "Centre x", "Centre y", "Radius"]
    # cell_df_current = pd.DataFrame(columns=cols)
    # cell_df_current = cell_df
    # for i in range(cell_df.shape[0]):
    #     clus_ID = cell_df.iloc[i,0]
    #     area_clus = cell_df.iloc[i,1]
    #     x_cen = cell_df.iloc[i,2]
    #     y_cen = cell_df.iloc[i,3]
    #     out_list, needed_of_final, radius = num_cir.order_segment(area_clus)
    #     # print(out_list)
    #     # print(needed_of_final)
    #     # points = num_cir.get_pixels(x_cen,y_cen, out_list, int(needed_of_final), clus_ID)
    #     # # # points_old = list(gen_points(cell_df.iloc[i,2],cell_df.iloc[i,3],cell_df.iloc[i,1],cell_df.iloc[i,0]))
    #     # for j in range(len(points)):
    #     #     all_pts = np.vstack([all_pts, points[j]])

    #     cell_df_current.loc[i] = [clus_ID, area_clus, x_cen, y_cen, radius]
    # print('Marker 1')
    coag_pairs = np.empty((0,2))
    coag_list = []
    coag_list_more_once = []
    coag_lists_df = pd.DataFrame(columns=["Coag IDs"])
    centres = np.empty((0,2))
    centre_x_moved = np.empty((0,2))
    centre_y_moved = np.empty((0,2))
    centre_both_moved = np.empty((0,2))
    move_x = False
    move_y = False
    move_both = False
    radii = []
    for e in range(cell_df.shape[0]):
        next_centre = [cell_df.iloc[e,2],cell_df.iloc[e,3]]
        centres = np.vstack([centres, next_centre])
        radius = cell_df.iloc[e,4]
        radii = np.append(radii, radius)

        if next_centre[0] <  radius:
            move_x = True
            #Close enough to the edge to include parts on the other side of periodic BC
            moved_x_centre = [int(cell_df.iloc[e,2]) + x_len, cell_df.iloc[e,3]]
            centre_x_moved = np.vstack([centre_x_moved, moved_x_centre])
        else:
            centre_x_moved = np.vstack([centre_x_moved, next_centre])

        if next_centre[1] <  radius:
            move_y = True
            #Close enough to the edge to include parts on the other side of periodic BC
            moved_y_centre = [cell_df.iloc[e,2], cell_df.iloc[e,3] + y_len]
            centre_y_moved = np.vstack([centre_y_moved, moved_y_centre])
        else:
            centre_y_moved = np.vstack([centre_y_moved, next_centre])
        
        if next_centre[0] <  radius and next_centre[1] < radius:
            move_both = True
            #Close enough to the edge to include parts on the other side of periodic BC
            moved_both_centre = [cell_df.iloc[e,2] + x_len, cell_df.iloc[e,3] + y_len]
            centre_both_moved = np.vstack([centre_both_moved, moved_both_centre])
        else:
            centre_both_moved = np.vstack([centre_both_moved, next_centre])
        



    centre_distances = self_distance(centres)

    radius_sums = radii[:, None] + radii[None, :]

    coag_arr_bool = np.greater_equal(radius_sums, centre_distances, dtype=bool)
    coag_arr_int = np.multiply(coag_arr_bool, 1)
    coag_arr_int = np.triu(coag_arr_int, k=1)

    coag_pairs_indices = np.argwhere(coag_arr_int > 0)

    # Periodic BCs
    if move_x == True:
        centre_distances = self_distance(centre_x_moved)

        radius_sums = radii[:, None] + radii[None, :]

        coag_arr_bool = np.greater_equal(radius_sums, centre_distances, dtype=bool)
        coag_arr_int = np.multiply(coag_arr_bool, 1)
        coag_arr_int = np.triu(coag_arr_int, k=1)

        coag_pairs_x_moved_indices = np.argwhere(coag_arr_int > 0)

        coag_pairs_indices = np.vstack([coag_pairs_indices, coag_pairs_x_moved_indices])
    
    if move_y == True:
        centre_distances = self_distance(centre_y_moved)

        radius_sums = radii[:, None] + radii[None, :]

        coag_arr_bool = np.greater_equal(radius_sums, centre_distances, dtype=bool)
        coag_arr_int = np.multiply(coag_arr_bool, 1)
        coag_arr_int = np.triu(coag_arr_int, k=1)

        coag_pairs_y_moved_indices = np.argwhere(coag_arr_int > 0)

        coag_pairs_indices = np.vstack([coag_pairs_indices, coag_pairs_y_moved_indices])

    if move_both == True:
        centre_distances = self_distance(centre_both_moved)

        radius_sums = radii[:, None] + radii[None, :]

        coag_arr_bool = np.greater_equal(radius_sums, centre_distances, dtype=bool)
        coag_arr_int = np.multiply(coag_arr_bool, 1)
        coag_arr_int = np.triu(coag_arr_int, k=1)

        coag_pairs_both_moved_indices = np.argwhere(coag_arr_int > 0)

        coag_pairs_indices = np.vstack([coag_pairs_indices, coag_pairs_both_moved_indices])

    # vfunc = np.vectorize(test_dist)
    # out1 = vfunc(centres[:,0], centres[:,1], centres[:,0], centres[:,1], radii, radii)
    
    # Get unique list of coag indices pairs
    coag_pairs_indices = np.unique(coag_pairs_indices, axis=0)
    print('Pairs Ind', coag_pairs_indices)

    for d in range(coag_pairs_indices.shape[0]):
        coag_ID_pair = [int(cell_df.iloc[coag_pairs_indices[d,0],0]),
                        int(cell_df.iloc[coag_pairs_indices[d,1],0])]
        if coag_ID_pair[0] in coag_list and coag_ID_pair[1] in coag_list:
            print('Both match')
            coag_list_more_once = np.append(coag_list_more_once, [coag_ID_pair])
            for m in range(coag_lists_df.shape[0]):
                if coag_ID_pair[0] in coag_lists_df.iloc[m,0]:
                    matching_1 = m
                    continue
            for n in range(coag_lists_df.shape[0]):
                if coag_ID_pair[1] in coag_lists_df.iloc[n,0]:
                    matching_2 = n
                    continue

            # if matching_1 == matching_2:
                # print('Already coagulating')
            # else:
            if matching_1 != matching_2:
                # Add 2nd row to 1st
                element_add = coag_lists_df.iloc[matching_1,0]
                element_add = element_add + coag_lists_df.iloc[matching_2,0]
                coag_lists_df.iloc[matching_1,0] = element_add

                coag_lists_df = coag_lists_df.reset_index()
                del coag_lists_df['index']
                # Drop 2nd row
                coag_lists_df = coag_lists_df.drop(matching_2)
            
        elif coag_ID_pair[0] in coag_list:
            print('1st match')
            coag_list_more_once = np.append(coag_list_more_once, coag_ID_pair[0])
            coag_list = np.append(coag_list, coag_ID_pair[1])
            for m in range(coag_lists_df.shape[0]):
                if coag_ID_pair[0] in coag_lists_df.iloc[m,0]:
                    element_add = coag_lists_df.iloc[m,0]
                    element_add.append(coag_ID_pair[1])
                    coag_lists_df.iloc[m,0] = element_add
                    continue

        elif coag_ID_pair[1] in coag_list:
            print('2nd match')
            coag_list_more_once = np.append(coag_list_more_once, coag_ID_pair[1])
            coag_list = np.append(coag_list, coag_ID_pair[0])
            for n in range(coag_lists_df.shape[0]):
                if coag_ID_pair[1] in coag_lists_df.iloc[n,0]:
                    element_add = coag_lists_df.iloc[n,0]
                    element_add.append(coag_ID_pair[0])
                    coag_lists_df.iloc[n,0] = element_add
                    continue
        else:
            coag_list = np.append(coag_list, [coag_ID_pair])
            coag_lists_df =pd.concat([coag_lists_df, pd.DataFrame([[coag_ID_pair]],  columns=["Coag IDs"])])


    # for h in range(centres.shape[0]):
    #     for g in range(centres.shape[0] - 1 - h):
    #         lower_cen = [centres.iloc[h,2],centres.iloc[h,3]]
    #         higher_cen = [centres.iloc[g + h + 1 ,2],centres.iloc[g + h + 1 ,3]]

    #         # Apply periodic BCs
    #         lower_x_change = [lower_cen[0] + x_len, lower_cen[1]]
    #         higher_x_change = [higher_cen[0] + x_len, higher_cen[1]]
    #         lower_y_change = [lower_cen[0], lower_cen[1] + y_len]
    #         higher_y_change = [higher_cen[0], higher_cen[1] + y_len]
    #         lower_both_change = [lower_cen[0] + x_len, lower_cen[1] + y_len]
    #         higher_both_change = [higher_cen[0] + x_len, higher_cen[1] + y_len]
    #         dist_between = min(math.dist(lower_cen, higher_cen),
    #                             math.dist(lower_x_change, higher_cen), math.dist(lower_y_change, higher_cen),
    #                             math.dist(lower_both_change, higher_cen),
    #                             math.dist(lower_cen, higher_x_change), math.dist(lower_cen, higher_y_change),
    #                             math.dist(lower_cen, higher_both_change))

    #         radius_sum = cell_df.iloc[g + h + 1,4] + cell_df.iloc[g + h + 1,4]

    #         if dist_between < radius_sum:
    #             # Coag candidates
    #             coag_ID_pair = [int(cell_df.iloc[h,0]), int(cell_df.iloc[g + h + 1 ,0])]
    #             coag_pairs = np.vstack([coag_pairs, coag_ID_pair])
    #             if coag_ID_pair[0] in coag_list and coag_ID_pair[1] in coag_list:
    #                 # print('Both match')
    #                 coag_list_more_once = np.append(coag_list_more_once, [coag_ID_pair])
    #                 for m in range(coag_lists_df.shape[0]):
    #                     if coag_ID_pair[0] in coag_lists_df.iloc[m,0]:
    #                         matching_1 = m
    #                         continue
    #                 for n in range(coag_lists_df.shape[0]):
    #                     if coag_ID_pair[1] in coag_lists_df.iloc[n,0]:
    #                         matching_2 = n
    #                         continue

    #                 # if matching_1 == matching_2:
    #                     # print('Already coagulating')
    #                 # else:
    #                 if matching_1 != matching_2:
    #                     # Add 2nd row to 1st
    #                     element_add = coag_lists_df.iloc[matching_1,0]
    #                     element_add = element_add + coag_lists_df.iloc[matching_2,0]
    #                     coag_lists_df.iloc[matching_1,0] = element_add

    #                     coag_lists_df = coag_lists_df.reset_index()
    #                     del coag_lists_df['index']
    #                     # Drop 2nd row
    #                     coag_lists_df.drop(matching_2)
    #                     # print('Multi-row for coag')
                    
    #             elif coag_ID_pair[0] in coag_list:
    #                 coag_list_more_once = np.append(coag_list_more_once, coag_ID_pair[0])
    #                 coag_list = np.append(coag_list, coag_ID_pair[1])
    #                 for m in range(coag_lists_df.shape[0]):
    #                     if coag_ID_pair[0] in coag_lists_df.iloc[m,0]:
    #                         element_add = coag_lists_df.iloc[m,0]
    #                         element_add.append(coag_ID_pair[1])
    #                         coag_lists_df.iloc[m,0] = element_add
    #                         continue
    #                 # location = np.where(coag_lists == coag_ID_pair[0])[0][0]
    #                 # coag_at_loc = coag_pairs[location]
    #                 # coag_at_loc = np.append(coag_at_loc, coag_ID_pair[1])
    #                 # print('Match 1st')
    #             elif coag_ID_pair[1] in coag_list:
    #                 coag_list_more_once = np.append(coag_list_more_once, coag_ID_pair[1])
    #                 coag_list = np.append(coag_list, coag_ID_pair[0])
    #                 for n in range(coag_lists_df.shape[0]):
    #                     if coag_ID_pair[1] in coag_lists_df.iloc[n,0]:
    #                         element_add = coag_lists_df.iloc[n,0]
    #                         element_add.append(coag_ID_pair[0])
    #                         coag_lists_df.iloc[n,0] = element_add
    #                         continue
    #                 # location = np.where(coag_lists == coag_ID_pair[1])[0][0]
    #                 # coag_at_loc = coag_pairs[location]
    #                 # coag_at_loc = np.append(coag_at_loc, coag_ID_pair[0])
    #                 # print('Match 2nd')
    #             else:
    #                 coag_list = np.append(coag_list, [coag_ID_pair])
    #                 coag_lists_df =pd.concat([coag_lists_df, pd.DataFrame([[coag_ID_pair]],  columns=["Coag IDs"])])

    for p in range(coag_lists_df.shape[0]):                
        cell_df, next_ID = Coagulation_overlap(cell_df, coag_lists_df.iloc[p,0], next_ID, x_len, y_len)


            # Avoid having to create the array at each point.
            # Check for clusters using loc and radius
        # multi_pair_IDs = []
        # for m in range(len(coag_list_more_once)):
        #     pairs_IDs = np.where(coag_list_more_once == coag_list_more_once[0])[0]
        #     for n in range(len(pairs_IDs)):
        #     # for n in range(len(coag_list_more_once) - m):
        #     #     multi_pair = np.where(coag_pairs == coag_list_more_once[m])[0]


            


        # # Apply periodic BCs
        # for k in range(all_pts.shape[0]):
        #     if all_pts[k,0] > x_len:
        #         all_pts[k,0] = all_pts[k,0] - x_len 
        #     if all_pts[k,1] > y_len:
        #         all_pts[k,1] = all_pts[k,1] - y_len
        #     if all_pts[k,0] <= 0:
        #         all_pts[k,0] = all_pts[k,0] + x_len 
        #     if all_pts[k,1] <= 0:
        #         all_pts[k,1] = all_pts[k,1] + y_len       

        # # check_for_coag
        # visual_arr = np.zeros((x_len,y_len))
        # for l in range(all_pts.shape[0]):
        #     visual_arr[int(all_pts[l,0])-1,int(all_pts[l,1])-1] += 1

        # overlap_locs = np.where(visual_arr > 1)
        # num_overlaps = len(overlap_locs[0])
        # # for m in range(num_overlaps):
        #     # Search all_pts for IDs
        # if num_overlaps > 0:
        #     x_search = overlap_locs[0][0] + 1
        #     y_search = overlap_locs[1][0] + 1

        #     x_vals = all_pts[:,0]
        #     y_vals = all_pts[:,1]
        #     x_match = np.where(x_vals == x_search)
        #     y_match = np.where(y_vals == y_search)
        #     # What happens if we have one of the clusters that's split over BCs
        #     # Move it all to the "positive" side and then find the average
        #     coag_indexes = np.intersect1d(x_match,y_match)

        #     coag_IDs = [int(all_pts[coag_indexes[0],2]),int(all_pts[coag_indexes[1],2])]

        #     # Store coag IDs
        #     cell_df, next_ID = Coagulation_overlap(cell_df, coag_IDs, next_ID, x_len, y_len)

            # ? Add Coagulation for neighbours here

    print('Sweep complete')
    print('Carried over IDs', cell_df['ID'].to_numpy())
    return cell_df, next_ID


def move_clusters(cell_df, x_len, y_len):

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
                # if x_cen < 0:
                #     x_cen += x_len
            elif r2 < 0.5:
                x_cen, y_cen = move_up(x_cen, y_cen)
                # if y_cen > y_len:
                #     y_cen -= y_len
            elif r2 < 0.75:
                x_cen, y_cen = move_right(x_cen, y_cen)
                # if x_cen > x_len:
                #     x_cen -= x_len
            else:
                x_cen, y_cen = move_down(x_cen, y_cen)
                # if y_cen < 0:
                #     y_cen += y_cen

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
        out_list, needed_of_final, radius = num_cir.order_segment(area_clus)
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

    # # check_for_coag
    # visual_arr = np.zeros((x_len,y_len))
    # for l in range(all_pts.shape[0]):
    #     visual_arr[int(all_pts[l,0])-1,int(all_pts[l,1])-1] += 1

    # # Just print locs
    visual_arr = np.zeros((x_len,y_len))
    for l in range(all_pts.shape[0]):
        if visual_arr[int(all_pts[l,0])-1,int(all_pts[l,1])-1] == 0:
            visual_arr[int(all_pts[l,0])-1,int(all_pts[l,1])-1] = 1

    return visual_arr

def self_distance(x):
    return np.linalg.norm(x[:,np.newaxis] - x, axis=-1)

def test_dist(a_1, a_2, b_1, b_2 ,r_a,r_b):
    if math.dist([a_1,a_2],[b_1,b_2]) < r_a + r_b:
        return 1
    else:
        return 0

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
    coag_IDs = np.sort(coag_IDs)
    print("IDs", coag_IDs)
    cols = ["ID", "Area", "Centre x", "Centre y", "Radius"]
    coag_df = pd.DataFrame(columns=cols)
    for i in range(len(coag_IDs)):
        index_drop = cell_df.index[cell_df['ID'] == coag_IDs[i]][0]
        print('Index drop', index_drop)
        if i == 0:
            coag_df = cell_df.loc[cell_df['ID'] == coag_IDs[i]]
        else:
            coag_df = pd.concat([coag_df, cell_df.loc[cell_df['ID'] == coag_IDs[i]]])
        cell_df = cell_df.drop(index_drop)
    # # Add check if centres are on opposite sides of periodic BCs
    # for j in range(len(coag_IDs) - 1):
    #     for k in range(len(coag_IDs) - j - 1):
    #         index_1 = j
    #         index_2 = j + k + 1
    # # if len(coag_IDs) == 2:
    #     if abs(coag_df.iloc[index_1,2] - coag_df.iloc[index_2,2]) > x_len/2:
    #         # Move centre from left to out right
    #         if coag_df.iloc[index_1,2] < coag_df.iloc[index_2,2]:
    #             coag_df.iloc[index_1,2] = coag_df.iloc[index_1,2] + x_len
    #         else:
    #             coag_df.iloc[index_2,2] = coag_df.iloc[index_2,2] + x_len

    #     if abs(coag_df.iloc[index_1,3] - coag_df.iloc[index_2,3]) > y_len/2:
    #         # Move centre from low to outside high value
    #         if coag_df.iloc[index_1,3] < coag_df.iloc[index_2,3]:
    #             coag_df.iloc[index_1,3] = coag_df.iloc[index_1,3] + y_len
    #         else:
    #             coag_df.iloc[index_2,3] = coag_df.iloc[index_2,3] + y_len
    # # Add check if centres are on opposite sides of periodic BCs
    # elif len(coag_IDs) > 2:
    #     print('Multi coag')
    #     sys.exit(0)
    # print(coag_df)
    new_ID = next_available_tag
    next_available_tag += 1
    
    new_area = coag_df.sum(axis=0).iloc[1]
    clus_ID = new_ID
    coag_all_pts = np.empty((0,3))
    x_sum = 0
    y_sum = 0
    for l in range(len(coag_IDs)):
        # clus_ID = coag_df.iloc[l,0]
        # area_clus = coag_df.iloc[l,1]
        x_sum += coag_df.iloc[l,2] * coag_df.iloc[l,1]
        y_sum += coag_df.iloc[l,3] * coag_df.iloc[l,1]
        # out_list, needed_of_final = num_cir.order_segment(area_clus)
        # print(out_list)
        # print(needed_of_final)
    new_centre_x = round(x_sum/new_area)
    new_centre_y = round(y_sum/new_area)
        # coag_points = num_cir.get_pixels(x_cen,y_cen, out_list, needed_of_final, clus_ID)

        # coag_points = list(gen_points(coag_df.iloc[i,2],coag_df.iloc[i,3],coag_df.iloc[i,1],coag_df.iloc[i,0]))
        # for m in range(len(coag_points)):
        #     coag_all_pts = np.vstack([coag_all_pts, coag_points[m]])

    # FInd average centre for new centre
            # If it crosses the BC that's fine because it's sorted in periodic BCs in visualise
            # It's possible to have 
    # new_centre_x = round(sum(coag_all_pts[:,0])/coag_all_pts.shape[0])
    # new_centre_y = round(sum(coag_all_pts[:,1])/coag_all_pts.shape[0])
    # if new_centre_x > x_len:
    #     new_centre_x = new_centre_x - x_len
    # if new_centre_y > y_len:
    #     new_centre_y = new_centre_y - y_len
    # cell_df.loc[len(cell_df.index)] = [new_ID, new_area, new_centre_x, new_centre_y]
    # create extension
    out_list, needed_of_final, radius = num_cir.order_segment(new_area)
    df_extended = pd.DataFrame(columns=cols)
    df_extended.loc[0] = [new_ID, new_area, new_centre_x, new_centre_y, radius]
    # print('New ID is', new_ID)

    # concatenate to original
    cell_df = pd.concat([cell_df, df_extended], ignore_index=True)

    return cell_df, next_available_tag