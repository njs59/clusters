def coagulation_event(rand, sum_coag, array):
# Coag event occurs
    shape = array.shape
    i_curr = 0
    j_curr = 1
    coag_cst = 1
    # coag_cst = coag_ker(0, i_curr, j_curr)
    chances = (coag_cst * (array[i_curr,0] + array[j_curr,0])/(array[i_curr,0] * array[j_curr,0]))/sum_coag
    while chances < rand:
        if j_curr == shape[0] - 1:
            i_curr += 1
            j_curr = i_curr + 1
        else:
            j_curr += 1
        # coag_cst = coag_ker(0, i_curr, j_curr)
        chances += (coag_cst * (array[i_curr,0] + array[j_curr,0])/(array[i_curr,0] * array[j_curr,0]))/sum_coag

    event_array = [i_curr, j_curr]
    return event_array

def coag_ker(ker, i, j):
    '''
    Define coagulation constants for different coagulation kernels 
    for clusters of sizes i & j
    ker = 0 : Constant kernel
    ker = 1 : DIffusive kernel
    '''
    if ker == 0:
        coag_cst = 1

    return coag_cst