import math
import numpy as np

import matplotlib.pyplot as plt

def order_segment(area_circle):
    centre = np.array([0, 0])
    out = np.array([0,0])
    candidates = np.array([0, 0 + 1])

    total_candidates_satisfying = 1
    while total_candidates_satisfying < area_circle:
        min_dist = math.inf
        min_dist_index = math.inf
        if candidates.ndim == 1:
            min_dist = math.dist(candidates, centre)
            selected_candidate = candidates
            # Remove candidate
            candidates = np.delete(candidates,(0,1), axis=0)
        else:
            for j in range(candidates.shape[0]):
                candidate_dist = math.dist(candidates[j], centre)
                if candidate_dist < min_dist:
                    min_dist = candidate_dist
                    min_dist_index = j
            selected_candidate = candidates[min_dist_index]
            # Remove selected candidate
            candidates = np.delete(candidates, (min_dist_index), axis=0)


        # Find how many will satisfy this condition of movement from centre
        # if np.array_equal(selected_candidate, [0,0]) == True:
        #     total_candidates_satisfying += 1
        if selected_candidate[0] == 0:
            # On axis
            total_candidates_satisfying += 4
        elif selected_candidate[0] == selected_candidate[1]:
            # On main diagonal
            total_candidates_satisfying += 4
        else:
            total_candidates_satisfying += 8

        # North always added, East needs checking if in list or if viable
        # Add North
        new_candidates = np.array([selected_candidate[0], selected_candidate[1] + 1])
        # Check for East
        east_x = selected_candidate[0] + 1
        east_y = selected_candidate[1]
        if np.array_equal(candidates, []) == True:
            if east_y >= east_x:
                new_candidates = np.vstack((new_candidates, [east_x, east_y]))
        else:
            if east_y >= east_x and [east_x, east_y] not in candidates:
                new_candidates = np.vstack((new_candidates, [east_x, east_y]))

        # Add new candidates
        if np.array_equal(candidates, []) == True:
            candidates = new_candidates
        else:
            candidates = np.vstack((candidates, new_candidates))

        out = np.vstack((out, selected_candidate))


    extras = total_candidates_satisfying - area_circle
    if area_circle == 1:
        needed_of_final = 0
    elif selected_candidate[0] == 0 or selected_candidate[0] == selected_candidate[1]:
        needed_of_final = 4 - extras
    else:
        needed_of_final = 8 - extras

    radius = math.dist(out[-1:][0], [0,0])

    return out, needed_of_final, radius



def get_pixels(x_cen, y_cen, out_list, needed_of_final, clus_ID):
    complete_path = out_list[:-1]
    final_path = out_list[-1]
    needed_of_final = int(needed_of_final)

    pixels_in_clus = np.array([])

    for i in range(complete_path.shape[0]):
        current_path = complete_path[i]
        if current_path[0] == 0 and current_path[1] == 0:
            # Centre case
            pixels_in_clus = np.array([x_cen, y_cen])
        elif current_path[0] == 0:
            # Main axis case
            change_1 = current_path[0]
            change_2 = current_path[1]
            pixels_to_add = np.array([[x_cen + change_1, y_cen + change_2], [x_cen + change_2, y_cen + change_1],
                                      [x_cen - change_1, y_cen - change_2], [x_cen - change_2, y_cen - change_1]])
            pixels_in_clus = np.vstack((pixels_in_clus, pixels_to_add))
        elif current_path[0] == current_path[1]:
            # Diagonal axis case
            change_1 = current_path[0]
            change_2 = current_path[1]
            pixels_to_add = np.array([[x_cen + change_1, y_cen + change_2], [x_cen + change_2, y_cen - change_1],
                                      [x_cen - change_1, y_cen - change_2], [x_cen - change_2, y_cen + change_1]])
            pixels_in_clus = np.vstack((pixels_in_clus, pixels_to_add))
        else:
            change_1 = current_path[0]
            change_2 = current_path[1]
            # Other case (8 possibilities)
            pixels_to_add = np.array([[x_cen + change_1, y_cen + change_2], [x_cen + change_2, y_cen + change_1],
                                      [x_cen + change_2, y_cen - change_1], [x_cen + change_1, y_cen - change_2],
                                      [x_cen - change_1, y_cen - change_2], [x_cen - change_2, y_cen - change_1],
                                      [x_cen - change_2, y_cen + change_1], [x_cen - change_1, y_cen + change_2]])
            pixels_in_clus = np.vstack((pixels_in_clus, pixels_to_add))

    # Final path, might not need all points
    current_path = final_path
    if current_path[0] == 0 and current_path[1] == 0:
        # Centre case
        pixels_in_clus = np.array([x_cen, y_cen])
    elif current_path[0] == 0:
        # Main axis case
        change_1 = current_path[0]
        change_2 = current_path[1]
        pixels_to_add = np.array([[x_cen + change_1, y_cen + change_2], [x_cen + change_2, y_cen + change_1],
                                    [x_cen - change_1, y_cen - change_2], [x_cen - change_2, y_cen - change_1]])
    elif current_path[0] == current_path[1]:
        # Diagonal axis case
        change_1 = current_path[0]
        change_2 = current_path[1]
        pixels_to_add = np.array([[x_cen + change_1, y_cen + change_2], [x_cen + change_2, y_cen - change_1],
                                    [x_cen - change_1, y_cen - change_2], [x_cen - change_2, y_cen + change_1]])
    else:
        # Other case (8 possibilities)
        change_1 = current_path[0]
        change_2 = current_path[1]
        pixels_to_add = np.array([[x_cen + change_1, y_cen + change_2], [x_cen + change_2, y_cen + change_1],
                                    [x_cen + change_2, y_cen - change_1], [x_cen + change_1, y_cen - change_2],
                                    [x_cen - change_1, y_cen - change_2], [x_cen - change_2, y_cen - change_1],
                                    [x_cen - change_2, y_cen + change_1], [x_cen - change_1, y_cen + change_2]])

    pixels_to_add = pixels_to_add[0:needed_of_final]
    
    pixels_in_clus = np.vstack((pixels_in_clus, pixels_to_add))

    pixels_in_clus = np.hstack((pixels_in_clus, np.full((pixels_in_clus.shape[0],1), clus_ID)))

    return pixels_in_clus

# out_list, needed_of_final, radius = order_segment(1000)
# print(out_list)
# print(needed_of_final)

# clus_pix = get_pixels(10,50, out_list, needed_of_final, clus_ID=23)

# print(clus_pix)
# print('Hit')
# x_max = 200
# y_max = 200
# arr_visual = np.zeros((x_max,y_max))
# for j in range(clus_pix.shape[0]):
#     loc = clus_pix[j]
#     loc_x = loc[0]
#     loc_y = loc[1]
#     if loc_x > x_max:
#         loc_x = loc_x - x_max
#     if loc_y > y_max:
#         loc_y = loc_y - y_max
#     if loc_x <= 0:
#         loc_x = loc_x + x_max
#     if loc_y <= 0:
#         loc_y = loc_y + y_max

#     arr_visual[loc_x - 1,loc_y - 1] += 1

# plt.imshow(arr_visual)
# plt.show()
