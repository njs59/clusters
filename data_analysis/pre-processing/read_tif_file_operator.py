import numpy as np
from osgeo import gdal as GD


def tif_to_arr(basedir, experiment, folder, well_loc, time_list, fileID, max_val):
  '''
  Reads in series of tif files and converts the pixel intensity to a single 3D array (3rd dimension is time)

  Inputs:
    Identify the experiment and where the tif files are stored
    basedir,
    experiment,
    folder,
    well_loc,

    time_list: list of deisred timepoints to read in
    fileID, this will be '.tif'

    max_val: eventual threshold value for pixel intensity, will be used here as a normalisation factor

  '''
  # Loop over timepoints
  for i in range(len(time_list)):
    # Read in tif file
    name_list_b = basedir, experiment, folder, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '_ORG', fileID
    name_list_b_2  =''.join(name_list_b)
    data_set_b = GD.Open(name_list_b_2)
    # Only interested in green channel (R is band 0, G is band 1, B is band 2)
    band_2 = data_set_b.GetRasterBand(1) # green channel
    b2 = band_2.ReadAsArray()
    # Stack on the 3rd dimension the pixel intensities
    img_1 = np.dstack((b2))

    im_1_adapted = np.zeros((img_1.shape[1],img_1.shape[2]))
    for j in range(img_1.shape[1]):
      for k in range(img_1.shape[2]):
        ## Main diffferences are in the green channel
        value = img_1[(0,j,k)]
        im_1_adapted[(j,k)] = value


    # max_val = img_1.max()
    # max_val = 330
    print('Normalisation val (maximum pixel intensity)', max_val)
    for l in range(img_1.shape[1]):
      for m in range(img_1.shape[2]):
        im_1_adapted[(l,m)] = im_1_adapted[(l,m)]/max_val



    if i == 0:
      main_array = im_1_adapted

    else:
      print(i)
      main_array = np.dstack((main_array, im_1_adapted))
      print(main_array.shape)
  
  return main_array