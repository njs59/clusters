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

    # reshaping the array from 3D
    # matrix to 2D matrix.
    arr_reshaped = tf_array_bool.reshape(tf_array_bool.shape[0], -1)
 
    # saving reshaped array to file.
    np.savetxt("/Users/Nathan/Documents/Oxford/DPhil/test_3D.txt", arr_reshaped)
 
    # retrieving data from file.
    loaded_arr = np.loadtxt("/Users/Nathan/Documents/Oxford/DPhil/test_3D.txt")
 
    load_original_arr = loaded_arr.reshape(
        loaded_arr.shape[0], loaded_arr.shape[1] // tf_array_bool.shape[2], tf_array_bool.shape[2])
    
    # check the shapes:
    print("shape of arr: ", tf_array_bool.shape)
    print("shape of load_original_arr: ", load_original_arr.shape)
    
    # check if both arrays are same or not:
    if (load_original_arr == tf_array_bool).all():
        print("Yes, both the arrays are same")
    else:
        print("No, both the arrays are not same")


    return tf_array_bool
