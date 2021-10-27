import time
from mainCam import hamamatsu_cam
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from skimage import io
import numpy as np
from dlp_functions import crafter6500
import threading


class cap():
    def newTrigCapture(self):
        self.dlp = crafter6500()
        self.pictures = []
        #self.cam.terminate()
        #self.loadPattern(flag=True)
        self.dlp.startSequence()
        time.sleep(1)
        self.startCam(1280, 960, 0, mode=0)
        for i in range(400):
            self.trigCount=i
            if (self.trigCount % 1 == 0):
                self.cam.stopAcquisiton()
                time.sleep(0.1)
                self.cam.startAcquisiton()
            self.dlp.gpio_active()
            # print("active after")d
            #time.sleep(0.5)
            time.sleep(0.01)
            temp = self.cam.takeCap()
            # print("cam after")
            self.pictures.append(temp)
            self.dlp.gpio_deactive()
            # print("deactive after")
            time.sleep(0.00001)
            #time.sleep(0.003)
            print(self.trigCount)
        self.kayit()
    def loadPattern(self,flag=False):
        self.dlp = crafter6500()
        self.dlp.loadPattern(flag)
    def loadPat2(self):
        self.dlp = crafter6500()
        self.dlp.loadPattern2()
    def startCam(self,width, heıght,camId,mode):
        self.cam = hamamatsu_cam()
        self.cam.createCamera(width, heıght,camId,mode=mode)
        if(mode==1):
            self.cam.start()
    def kayit(self):
        for i in range(400):
            img = np.array(self.pictures[i]).reshape(2048, 2048)
            io.imsave('04_10_2021_9p1p/test{}.tif'.format(i), img)
            print("kayıt")
        self.cam.terminate()


deneme = cap()
deneme.newTrigCapture()
#deneme.loadPat2()