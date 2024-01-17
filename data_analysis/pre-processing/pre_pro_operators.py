import numpy as np

def threshold_arr(img_1):
    im_1_adapted = np.zeros((img_1.shape[1],img_1.shape[2]))
    for j in range(img_1.shape[1]):
      for k in range(img_1.shape[2]):
        ## Main diffferences are in the green channel
        value = img_1[(0,j,k)]
        im_1_adapted[(j,k)] = value


    max_val = img_1.max()
    for l in range(img_1.shape[1]):
      for m in range(img_1.shape[2]):
        im_1_adapted[(l,m)] = im_1_adapted[(l,m)]/max_val


    tf_array_bool = np.array(tf_array, dtype = bool)

    if i == 0:
      main_array = tf_array_bool

    else:
      print(i)
      main_array = np.dstack((main_array, tf_array_bool))
      print(main_array.shape)