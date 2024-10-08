from PIL.ExifTags import TAGS
import pathlib
import csv

import glob
from PIL import Image
import pandas as pd

image = Image.open('/Users/Nathan/Documents/Oxford/DPhil/2017-02-03_sphere_timelapse/' +
                 'RAW/Timelapse/sphere_timelapse_useful_wells/sphere_timelapse_s11t51c2_ORG.tif')

   
# extract other basic metadata
info_dict = {
    "Filename": image.filename.split('/')[1],
    "Image Size": image.size,
    "Image Height": image.height,
    "Image Width": image.width,
    "Image Format": image.format,
    "Image Mode": image.mode,
    "Image is Animated": getattr(image, "is_animated", False),
    "Frames in Image": getattr(image, "n_frames", 1),
}

print(info_dict)

# info.append(info_dict)