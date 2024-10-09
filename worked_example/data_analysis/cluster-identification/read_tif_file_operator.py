import numpy as np
from osgeo import gdal as GD


def tif_to_arr(naming_convention_pre_number, naming_convention_post_number, time_list):
  '''
  Reads in series of tif files and converts the pixel intensity to a single 3D array (3rd dimension is time)

  Inputs:
    Identify the experiment and where the tif files are stored
      naming_convention_pre_number: naming convention before the time array number
      naming_convention_post_number: naming convention after the time array number
      time_list: list of desired timepoints to read in



  '''
  # Loop over timepoints
  for i in range(len(time_list)):
    name_list = naming_convention_pre_number, time_list[i], naming_convention_post_number
    name_list_joined  =''.join(name_list)
    data_set = GD.Open(name_list_joined)
    # Only interested in green channel (R is band 0, G is band 1, B is band 2)
    band = data_set.GetRasterBand(1) # green channel
    slice_arr = band.ReadAsArray()
    # img_1 = np.dstack((b2))
    
    # Store normalised intensities in 3D array
    if i == 0:
      main_array = slice_arr

    else:
      print(i)
      main_array = np.dstack((main_array, slice_arr))
      print(main_array.shape)

  # Output 3D normalised array
  return main_array