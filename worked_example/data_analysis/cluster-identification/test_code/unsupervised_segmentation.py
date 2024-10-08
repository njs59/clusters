import numpy as np
import matplotlib.pyplot as plt

import skimage.data as data
import skimage.segmentation as seg
from skimage import filters
from skimage import draw
from skimage import color
from skimage import exposure
from scipy.ndimage.filters import median_filter

from PIL import Image, ImageFilter
import read_tif_file_operator as tif


#Import the necessary libraries 
import cv2 
import matplotlib.pyplot as plt 
import numpy as np 

# from squidpy import ImageContainer, segment


def image_show_save(image):
    plt.imshow(image, cmap='gray')
    plt.axis([0, image.shape[1], 0, image.shape[0]])
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
#experiment = 'RAW_data/2017-02-13_sphere_timelapse_2/'
#exp_date = '2017-02-13'
folder = 'RAW/Timelapse/sphere_timelapse_useful_wells/'
fileID = '.tif'
time_list = range(42,98,5)
well_loc = 's11'


for i in range(67,68,1):
    time = i

    raw_arr_2D = tif.tif_to_arr(basedir, experiment, folder, well_loc, str(time), fileID)

    raw_arr_2D = raw_arr_2D[:,1:]
    # raw_arr_2D -= raw_arr_2D.min()
    # raw_arr_2D *= 10

    # text = data.page()
    image_show_save(raw_arr_2D)

    text_threshold = filters.threshold_yen  # Hit tab with the cursor after the underscore, try several methods
    thresh = text_threshold(raw_arr_2D)
    array = raw_arr_2D > thresh
    image_show(raw_arr_2D > thresh)
    print("Threshold is", thresh)

    plt.imshow(array, cmap='gray')
    plt.axis('off')
    plt.savefig('PRO_Yen.png', dpi=300)
    # plt.hist(raw_arr_2D)
    # plt.show()

# to_segment = ImageContainer(raw_arr_2D)
# segmented = segment(img  = to_segment, channel = 0, method = 'watershed', geq = True)

# plt.imshow(segmented)
# plt.show()




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


# original= raw_arr_2D
# # plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
# # plt.axis('off')  # Remove axis labels
# # plt.show()
# # print("Blur Image")

# # # create a sharpening kernel
# # sharpen_filter=np.array([[-1, -1, -1, -1, -1, -1, -1],
# #                    [-1, -1, -1, -1, -1, -1, -1],
# #                    [-1, -1, -1, -1, -1, -1, -1],
# #                    [-1, -1, -1, 49, -1, -1, -1],
# #                    [-1, -1, -1, -1, -1, -1, -1],
# #                    [-1, -1, -1, -1, -1, -1, -1],
# #                    [-1, -1, -1, -1, -1, -1, -1]])
# # # applying kernels to the input image to get the sharpened image

# # sharp_image=cv2.filter2D(original,-1,sharpen_filter)
# # image_show_save(sharp_image)

# # print("Sharpened Image")

# # original_image = raw_arr_2D

# blur_image = cv2.blur(raw_arr_2D,(10,10)) 

# image_show_save(blur_image)

# blur_2_image = cv2.blur(blur_image,(10,10)) 

# image_show_save(blur_2_image)




# image_show_save(raw_arr_2D)

# text_threshold = filters.threshold_yen  # Hit tab with the cursor after the underscore, try several methods
# thresh = text_threshold(raw_arr_2D)
# array = raw_arr_2D > thresh
# image_show(raw_arr_2D > thresh)


# text_threshold = filters.threshold_yen  # Hit tab with the cursor after the underscore, try several methods
# thresh = text_threshold(blur_image)
# array = raw_arr_2D > thresh
# image_show(raw_arr_2D > thresh)

# text_threshold = filters.threshold_yen  # Hit tab with the cursor after the underscore, try several methods
# thresh = text_threshold(blur_2_image)
# array = raw_arr_2D > thresh
# image_show(raw_arr_2D > thresh)