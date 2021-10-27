import cv2
import numpy as np
from skimage import io

import cv2

image = cv2.imread('images/images/test0.tif')


for i in range(1,390):
    temp = cv2.imread('images/images/test0.tif')
    image = image+temp


io.imsave('images/totall.tif',image)

