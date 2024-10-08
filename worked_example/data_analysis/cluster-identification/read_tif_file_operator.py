import numpy as np
from osgeo import gdal as GD


def tif_to_arr(name_list):
  '''
  Reads in tif file and converts the pixel intensity to a single 2D array

  Inputs:
    name_list - path to raw data file




  '''
  data_set_b = GD.Open(name_list)
  # Only interested in green channel (R is band 0, G is band 1, B is band 2)
  band_2 = data_set_b.GetRasterBand(1) # green channel
  out_array = band_2.ReadAsArray()

  return out_array