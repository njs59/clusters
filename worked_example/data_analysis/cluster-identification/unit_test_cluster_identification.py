import math
import numpy as np
import numpy.testing as npt

import unittest

import cluster_identification_operators as iden_oper
import read_tif_file_operator as read_tif

from pylab import *
from scipy.ndimage import *

import matplotlib.pyplot as plt
import random


class TestPreProOperators(unittest.TestCase):

    def test_threshold_arr_supervised(self):
        # Parameters are (tf_array, threshold)

        test_tf_array = np.array([[[0,1],[1,2]],[[2,2],[0,0]]])
        test_bool = iden_oper.threshold_arr_supervised(test_tf_array, 1)

        self.assertTrue(np.all(test_bool == np.array([[[0,0],[0,1]],[[1,1],[0,0]]])))

    def test_bool_threshold_val(self):
        # Parameters are (a, threshold)

        test_1 = iden_oper.bool_threshold_val(3,2)
        self.assertEqual(test_1,1)
        test_2 = iden_oper.bool_threshold_val(2,2)
        self.assertEqual(test_2,0)
        test_3 = iden_oper.bool_threshold_val(1,2)
        self.assertEqual(test_3,0)


    def test_threshold_arr_unsupervised(self):
        # Parameters are (tf_array)

        test_tf_array = np.array([[[0,1],[1,200]],[[200,2],[0,0]]])
        folder = "/Users/Nathan/Documents/Oxford/DPhil/In_vitro_homogeneous_data/RAW_data/2017-02-03_sphere_timelapse/RAW/Timelapse/sphere_timelapse_useful_wells/"
        time_array = range(67,69)
        time_list = [str(x).zfill(2) for x in time_array]
        test_tf_array = read_tif.tif_to_arr("", "", folder, "s11", time_list, '.tif')

        test_bool = iden_oper.threshold_arr_unsupervised(test_tf_array)
        
        arr = np.loadtxt("/Users/Nathan/Documents/Oxford/DPhil/In_vitro_homogeneous_data/pre_processing_output/2017-02-03/s11t67c2_area.csv",
                 delimiter=",", dtype=int)
        arr = arr > 0
        array = test_bool[:,:,0]*1
        arr = arr*1

        diff_arr = np.subtract(array,arr)
        print("max is",np.max(diff_arr))

        # Label the clusters of the boolean array
        label_arr, num_clus = label(diff_arr)


        # Get a 1D list of areas of the clusters
        area_list = sum(diff_arr, label_arr, index=arange(label_arr.max() + 1))

        # plt.imshow(diff_arr)
        # plt.show()

        # Assert each difference cluster is smaller than 150 so will be removed in remove_fragments
        self.assertTrue(np.max(area_list) < 150)

    def test_remove_fragments(self):
        # Parameters are (area, num_clus, min_clus_size)

        area = np.array([0,100,2,300,4,500])

        
        area_new, index_keep = iden_oper.remove_fragments(area, 5, 150)
        print('Outputs', area_new,index_keep)
        self.assertTrue(np.all(area_new == np.array([300,500])))
        self.assertTrue(np.all(index_keep == np.array([3,5])))
        



if __name__ == '__main__':
    unittest.main()