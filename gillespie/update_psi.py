import numpy as np

def update_master(psi, index):
    '''
    Function to update psi with new distribution once equation of iven index is applied

    Input:
    psi: distribution to be updated
    index: Integer between 0 and 5196 for python subscript of corresponding equation
    '''
    if index in range(0, 2500):
        ## COagulation update
        Stuff
    elif index in range(2500, 2599):
        ## Mitosis update
        psi[index - 2500] -= 1 # Remove 1 cluster of size i
        psi[index - 2500 + 1] += 1 # Add 1 cluster of size i+1
    elif index in range(2599, 2698):
        ## Death update
        Stuff
    elif index in range(2698, 5197):
        ## Splitting update
        Stuff