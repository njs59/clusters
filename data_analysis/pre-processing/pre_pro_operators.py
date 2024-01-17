import numpy as np

def threshold_arr(tf_array, threshold):
    tf_ad = tf_array
    for p in range(tf_array.shape[0]):
      for q in range(tf_array.shape[1]):
        for r in range(tf_array.shape[2]):
            if tf_array[(p,q,r)] > threshold:
                tf_ad[(p,q,r)] = 1
            else:
                tf_ad[(p,q,r)] = 0

    # tf_array_bool = np.array(tf_ad, dtype = bool)
    tf_array_bool = tf_ad
    return tf_array_bool
