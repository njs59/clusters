def shedding_event(rand, shed_cst, sum_coag, sum_shed, array):
    shape = array.shape
    total_sum = sum_coag + sum_shed

    # Shed event occurs
    k_curr = 0
    shed_cst = 1
    # shed_cst = shed_ker(1,k_curr)
    chances_shed = (shed_cst * (array[k_curr,1]))/sum_shed
    shed_found = False

    while shed_found == False:
        if k_curr == shape[0]:
            print('Attempted impossible shedding')
            event_array = []
            shed_found = True
        elif array[k_curr,1] <= 1:
            k_curr += 1
        else:
            # shed_cst = shed_ker(1,k_curr)
            chances_shed += (shed_cst * (array[k_curr,1]))/sum_shed
            if (sum_coag/total_sum) + chances_shed > rand:
                shed_found = True
            else:
                k_curr += 1
        
    event_array = [k_curr]
    return event_array


def shed_ker(ker, i):
    '''
    Define shedding constants for different shedding kernels 
    for clusters of size i
    ker = 0 : Constant kernel
    '''
    if ker == 0:
        coag_cst = 1

    return coag_cst