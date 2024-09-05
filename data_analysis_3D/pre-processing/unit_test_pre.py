import math
import numpy as np
import numpy.testing as npt

import unittest

import pre_pro_operators as pre_oper
import read_tif_file_operator as read_tif

import random


class TestPreProOperators(unittest.TestCase):

    def test_threshold_arr_supervised(self):
        # Parameters are (tf_array, threshold)

        test_tf_array = np.array([[[0,1],[1,2]],[[2,2],[0,0]]])
        test_bool = pre_oper.threshold_arr_supervised(test_tf_array, 1)

        self.assertTrue(np.all(test_bool == np.array([[[0,0],[0,1]],[[1,1],[0,0]]])))

    def test_bool_threshold_val(self):
        # Parameters are (a, threshold)

        test_1 = pre_oper.bool_threshold_val(3,2)
        self.assertEqual(test_1,1)
        test_0 = pre_oper.bool_threshold_val(2,2)
        self.assertEqual(test_0,0)
        test_0 = pre_oper.bool_threshold_val(1,2)
        self.assertEqual(test_0,0)



        



if __name__ == '__main__':
    unittest.main()