import skimage.io
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage import data, img_as_float
from scipy import ndimage as ndi
from functions import SIM


coordinates = []

for j in range(400):

    image = skimage.io.imread("C:/Users/optof/PycharmProjects/basic_HamamatsuControl/images/images/test{}.tif".format(j), plugin='tifffile')
    sim = SIM()
    image = sim.bytescaling(image)
    image = image[750:1500, 500:1250]

    result_copy = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_GRAY2BGR)

    ret3, th3 = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(th3.astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = []

    for i in range(len(contours)):
        sum_x = 0
        sum_y = 0
        for point in contours[i]:
            sum_x += point[0][0]
            sum_y += point[0][1]
        center_x = sum_x / len(contours[i])
        center_y = sum_y / len(contours[i])
        cnts.append((center_x,center_y))
        cv2.circle(result_copy, (int(center_x), int(center_y)), 2, (0, 0, 255), -1)
    np.save("Coordinates/c{}.npy".format(j), np.array(cnts))
    #cv2.imwrite("result/result{}.png".format(j), result_copy)

