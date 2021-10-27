# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 12:37:29 2021

@author: optof
"""
import skimage.io
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage import data, img_as_float
from scipy import ndimage as ndi


class SIM():
    
    def bytescaling(self,data, cmin=None, cmax=None, high=255, low=0):
        """
        Converting the input image to uint8 dtype and scaling
        the range to ``(low, high)`` (default 0-255). If the input image already has
        dtype uint8, no scaling is done.
        :param data: 16-bit image data array
        :param cmin: bias scaling of small values (def: data.min())
        :param cmax: bias scaling of large values (def: data.max())
        :param high: scale max value to high. (def: 255)
        :param low: scale min value to low. (def: 0)
        :return: 8-bit image data array
        """
        if data.dtype == np.uint8:
            print("normal")
            return data

        if high > 255:
            high = 255
        if low < 0:
            low = 0
        if high < low:
            raise ValueError("`high` should be greater than or equal to `low`.")

        if cmin is None:
            cmin = data.min()
            print(cmin)
        if cmax is None:
            cmax = data.max()
            print(cmax)

        cscale = cmax - cmin
        if cscale == 0:
            cscale = 1

        scale = float(high - low) / cscale
        bytedata = (data - cmin) * scale + low
        return (bytedata.clip(low, high) + 0.5).astype(np.uint8)
    
    def crop_image(self,im, unet_input_size, shift_x, shift_y):
        size_im = im.shape
        pad_size_x, pad_size_y = 0, 0
        if size_im[0] % unet_input_size != 0:
            pad_size_y = (size_im[0] // unet_input_size + 1) * unet_input_size - size_im[0]
        if size_im[1] % unet_input_size != 0:
            pad_size_x = (size_im[1] // unet_input_size + 1) * unet_input_size - size_im[1]
    
        pad_im = np.pad(im, ((shift_y, pad_size_y + shift_y), (shift_x, pad_size_x + shift_x)),
                        mode='mean')  # )mode='constant',constant_values=0
        size_pad_im = pad_im.shape
        x_div, y_div = np.int64(size_pad_im[1] / unet_input_size), np.int64(size_pad_im[0] / unet_input_size)
    
        im_cropped = []
        count = 0
        for j in range(y_div):
            for i in range(x_div):
                cropped = pad_im[j * unet_input_size:(j + 1) * unet_input_size,
                          i * unet_input_size:(i + 1) * unet_input_size]
                im_cropped.append(np.uint8(cropped))
                count = count + 1
    
        return im_cropped
    
    def merge_image(self,images, cr_sizeX, cr_sizeY, fullResX, fullResY, shift_x, shift_y):
        v_images = []
        y_scan = fullResY // cr_sizeY 
        x_scan = fullResX // cr_sizeX 
        for i in range(y_scan):
            v_img = cv2.hconcat(images[(i * x_scan):((i * x_scan) + x_scan)])
            v_images.append(v_img)
        image_full = cv2.vconcat(v_images)
        return image_full[shift_y:fullResY + shift_y, shift_x:fullResX + shift_x]
    
    def adjust_gamma(self,image, gamma=1.0):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)
    
    
    def background_subtraction(self,image,background):
        background_blur = cv2.GaussianBlur(background,(1001,1001),0)
        gray_background=background_blur/background.max()
        gray=image/gray_background 
        print(gray[0:50])
        return gray.astype("uint8")
    
    
    def distance(point1,point2):
        result= ((((point2[0] - point1[0] )**2) + ((point2[1]-point1[1])**2) )**0.5)
        return result
    
 