import sys
import os
import time
import cv2
import threading
import numpy as np
import signal
import json
from PySide2 import  QtCore,QtGui,QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from skimage import io
from pypylon import pylon
import cv2
import numpy as np
from hamamatsuCamera import HamamatsuCamera

class hamamatsu_cam(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    change_signal_maxValue = Signal(int)
    change_pixmap_signal_focus = Signal(np.ndarray)
    _running = True
    def createCamera(self,width,heıght,camId,mode):
        self.hcam = HamamatsuCamera(0,mode)
        print(self.hcam.setPropertyValue("defect_correct_mode", 1))
        print("camera 0 model:", self.hcam.getModelInfo(0))
        print("Supported properties:")
        #props = self.hcam.getProperties()
        #for i, id_name in enumerate(sorted(props.keys())):
        #    [p_value, p_type] = self.hcam.getPropertyValue(id_name)
        #    p_rw = self.hcam.getPropertyRW(id_name)
        #    read_write = ""
        #   if (p_rw[0]):
        #        read_write += "read"
        #    if (p_rw[1]):
        #        read_write += ", write"
        #    print("  %s)%s = %s type is:%s,%s" % (i, id_name, p_value, p_type, read_write))
        #    text_values = self.hcam.getPropertyText(id_name)
        #    if (len(text_values) > 0):
        #        print("          option / value")
        #        for key in sorted(text_values, key=text_values.get):
        #            print("         %s/%s" % (key, text_values[key]))
        if mode==0:
            print(self.hcam.setPropertyValue("exposure_time", 0.3))
            self.hcam.setPropertyValue("trigger_source", 3)
            self.hcam.setPropertyValue("trigger_mode", 1)
            self.hcam.setPropertyValue("trigger_active",1)
            # print(hcam.setPropertyValue("subarray_hsize", 2048))
            # print(hcam.setPropertyValue("subarray_vsize", 2048))
            print(self.hcam.setPropertyValue("subarray_hpos", 0))
            print(self.hcam.setPropertyValue("subarray_vpos", 0))
            print(self.hcam.setPropertyValue("subarray_hsize", 2048))
            print(self.hcam.setPropertyValue("subarray_vsize", 2048))

            print(self.hcam.setPropertyValue("binning", "1x1"))
            print(self.hcam.setPropertyValue("readout_speed", 2))

            #self.hcam.setSubArrayMode()
            self.hcam.startAcquisition()
            #self.hcam.stopAcquisition()
            #self.hcam.dcam.dcamcap_start()
            time.sleep(0.1)
            #self.cam.startAcquisiton()


            params = ["internal_frame_rate",
                      "timing_readout_time",
                      "exposure_time",
                      "image_height",
                      "image_width",
                      "image_framebytes",
                      # "buffer_framebytes",
                      # "buffer_rowbytes",
                      # "buffer_top_offset_bytes",
                      "subarray_hsize",
                      "subarray_vsize",
                      "binning"]

            for param in params:
                print(param, self.hcam.getPropertyValue(param)[0])
        else:
            print(self.hcam.setPropertyValue("exposure_time", 0.3))
            # print(hcam.setPropertyValue("subarray_hsize", 2048))
            # print(hcam.setPropertyValue("subarray_vsize", 2048))
            print(self.hcam.setPropertyValue("subarray_hpos", 0))
            print(self.hcam.setPropertyValue("subarray_vpos", 0))
            print(self.hcam.setPropertyValue("subarray_hsize", 2048))
            print(self.hcam.setPropertyValue("subarray_vsize", 2048))

            print(self.hcam.setPropertyValue("binning", "1x1"))
            print(self.hcam.setPropertyValue("readout_speed", 2))

            # self.hcam.setSubArrayMode()
            self.hcam.startAcquisition()
            # self.hcam.stopAcquisition()
            #self.hcam.dcam.dcamcap_start()
            time.sleep(0.1)
            # self.cam.startAcquisiton()

            params = ["internal_frame_rate",
                      "timing_readout_time",
                      "exposure_time",
                      "image_height",
                      "image_width",
                      "image_framebytes",
                      # "buffer_framebytes",
                      # "buffer_rowbytes",
                      # "buffer_top_offset_bytes",
                      "subarray_hsize",
                      "subarray_vsize",
                      "binning"]

            for param in params:
                print(param, self.hcam.getPropertyValue(param)[0])



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
        if cmax is None:
            cmax = data.max()

        cscale = cmax - cmin
        if cscale == 0:
            cscale = 1

        scale = float(high - low) / cscale
        bytedata = (data - cmin) * scale + low
        return (bytedata.clip(low, high) + 0.5).astype(np.uint8)

    def setExposure(self,value):
        a = float(value)
        self.hcam.setPropertyValue("exposure_time", a)
        print(a)


    def setGain(self,value):
        pass

    def setRoi(self,width,height,offsetX,offsetY):
        pass

    def takeCap(self):
        self.hcam.fireTrigger()
        time.sleep(0.1)
        [frames, dims] = self.hcam.getFrames()
        for aframe in frames:
            temp = aframe.getData()
        return temp

    def startAcquisiton(self):
        self.hcam.startAcquisition()
    def stopAcquisiton(self):
        self.hcam.stopAcquisition()



    def terminate(self):
        self._running = False
        self.hcam.stopAcquisition()
        self.hcam.shutdown()

    def run(self):
        #self.hcam.startAcquisition()
        while self._running:
            # hcam.startAcquisition()
            [frames, dims] = self.hcam.getFrames()
            # hcam.stopAcquisition()
            for aframe in frames:
                self.img = aframe.getData()
                temp_max_value = np.amax(self.img)
                #temp_max_value = np.mean(self.img)
            self.imS = self.img.reshape(2048, 2048)
            final = self.bytescaling(self.imS)
            #cv2.imwrite("hams.png",final)
            self.change_pixmap_signal.emit(final)
            self.change_signal_maxValue.emit(temp_max_value)

    def saveImage(self):
        io.imsave('test_16bit.tif', self.imS)

