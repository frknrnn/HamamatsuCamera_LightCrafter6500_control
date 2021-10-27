import numpy as np
import cv2
import skimage.io
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage import data, img_as_float
from scipy import ndimage as ndi
from functions import SIM

def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)


x2r = np.zeros((1500,1500))
image = skimage.io.imread("C:/Users/optof/PycharmProjects/basic_HamamatsuControl/images/images/test{}.tif".format(0), plugin='tifffile')
c = image[750:1500, 500:1250]
coor = np.load("Coordinates/c{}.npy".format(0))
gaus =  makeGaussian(10)
print(coor)

for i in range(len(coor)):
    temp_m = np.zeros((10,10))
    x=int(coor[i][0])
    y=int(coor[i][1])
    for i in range(10):
        for j in range(10):
            if(x-5+i<750 and y-5+j<750):
                temp_v = c[x - 5 + i, y - 5 + j]
            else:
                temp_v = 0
            if(x-5+i<0):
                temp_v = 0
            if (y - 5 + j < 0):
                temp_v = 0
            temp_m[i,j] =temp_v
    after_g_m = temp_m*gaus
    x2r[(2*x)-5:(2*x)+5,(2*y)-5:(2*y)+5]=after_g_m

print(x2r)







