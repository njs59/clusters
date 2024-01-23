import numpy as np
from osgeo import gdal as GD


def tif_to_arr(basedir, experiment, folder, well_loc, time_list, fileID, max_val):
  for i in range(len(time_list)):
    name_list_b = basedir, experiment, folder, 'sphere_timelapse_', well_loc, 't', time_list[i], 'c2', '_ORG', fileID
    name_list_b_2  =''.join(name_list_b)
    data_set_b = GD.Open(name_list_b_2)
    # Only interested in green channel
    band_2 = data_set_b.GetRasterBand(1) # green channel
    b2 = band_2.ReadAsArray()
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