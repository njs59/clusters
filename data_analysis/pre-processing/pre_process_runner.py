from osgeo import gdal as GD
import matplotlib.pyplot as plt
import numpy as np

import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
from skimage import io
from PIL import Image

from pylab import *
from scipy.ndimage import measurements

from scipy.ndimage import *

basedir = '/content/drive/MyDrive/'


experiment = '2017-02-03_sphere_timelapse/'
folder = 'RAW/Timelapse/sphere_timelapse/'
folder_3 = 'sphere_timelapse/'

fileID = '.tif'

time_array = range(1,31)

time_list = [str(x).zfill(2) for x in time_array]


# reprT = ['01','07','13','19','25','31','37','43','49','55','61','67','73','79','85','91','97']
reprT = ['21','22','23','24','25','26','27','28','29','30']
#,'31','32','33','34','35','36','37','38','39','40',
#        '41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60']
# reprT = ['01','02','07','13']

well_loc = 's11'