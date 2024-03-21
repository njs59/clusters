import numpy as np
import matplotlib.pyplot as plt

import skimage.data as data
import skimage.segmentation as seg
from skimage import filters
from skimage import draw
from skimage import color
from skimage import exposure

import read_tif_file_operator as tif


#Import the necessary libraries 
import cv2 
import matplotlib.pyplot as plt 
import numpy as np 


def image_show_save(image):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.savefig('test_un.jpg')
    plt.show()

def image_show(image):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()


###    -----------   Input parameters   --------------     ###
basedir = '/Users/Nathan/Documents/Oxford/DPhil/In_vitro_homogeneous_data/'
experiment = 'RAW_data/2017-02-03_sphere_timelapse/'
exp_date = '2017-02-03'
# experiment = 'RAW_data/2017-02-13_sphere_timelapse_2/'
# exp_date = '2017-02-13'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
fileID = '.tif'
time = 65
well_loc = 's09'




raw_arr_2D = tif.tif_to_arr(basedir, experiment, folder, well_loc, time, fileID)


# text = data.page()
image_show_save(raw_arr_2D)


# # Load the image 
# image = cv2.imread('test_un.jpg') 
  
# #Plot the original image 
# plt.subplot(1, 2, 1) 
# plt.title("Original") 
# plt.imshow(image) 
  
# # Remove noise using a Gaussian filter 
# sharpened_image = cv2.GaussianBlur(image, (3, 3), 0) 
  
# #Save the image 
# cv2.imwrite('Gaussian Blur.jpg', sharpened_image)
  

  
# #Plot the sharpened image 
# plt.subplot(1, 2, 2) 
# plt.title("Sharpening") 
# plt.imshow(sharpened_image) 
# plt.show()
# sharpened_2D = sharpened_image[:,:,1]
# raw_arr_2D = np.asarray(sharpened_2D)

# raw_arr_2D = np.multiply(raw_arr_2D, 10)

image_show_save(raw_arr_2D)

text_threshold = filters.threshold_yen  # Hit tab with the cursor after the underscore, try several methods
thresh = text_threshold(raw_arr_2D)
array = raw_arr_2D > thresh
image_show(raw_arr_2D > thresh)