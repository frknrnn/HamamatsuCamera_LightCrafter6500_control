import pycrafter6500
import numpy as np
import cv2

class crafter6500():

    def __init__(self):
        self.dlp = pycrafter6500.dmd()
        self.dlp.stopsequence()

    def dlp_mode(self,value):
        self.dlp.changemode(value)

    def startSequence(self):
        self.dlp.startsequence()
    def stopSequence(self):
        self.dlp.stopsequence()
    def pauseSequence(self):
        pass

    def gpio_active(self):
        self.dlp.gpıo0_a()
        self.dlp.checkforerrors()
    def gpio_deactive(self):
        self.dlp.gpıo0_d()
        self.dlp.checkforerrors()

    def loadPattern(self,trig_flag):
        #self.dlp.stopsequence()
        # deneme
        images = []
        count = 10
        for i in range(10):
            path = "Pattern/pattern1/dot10_0{}.tif".format(i)
            print(path)
            img = cv2.imread(path, 0)/255
            images.append(np.array(img))
            print(np.amax(images))
            print(np.array(images).shape)
        self.dlp.stopsequence()
        self.dlp.changemode(3)
        exposure = [500000] * count
        dark_time = [0] * count
        trigger_in = []
        for i in range(count):
            trigger_in.append(trig_flag)
        # trigger_in=[False]*90
        trigger_out = [1] * count
        #images = np.array(images, dtype=np.uint8)
        self.dlp.defsequence(images, exposure, trigger_in, dark_time, trigger_out, 0)
        self.dlp.startsequence()

    def loadPattern2(self):
        self.dlp.stopsequence()
        images = []
        count = -1

        for x in range(0, 20, 1):
            for y in range(0, 20, 1):
                count = count + 1
                print(count)
                pattern = np.zeros((1200, 2000))

                for i in range(1200):
                    for j in range(2000):
                        if (i % 20 == 0):
                            if ((i // 20) % 2 == 0):
                                if (j % 20 == 0):
                                    pattern[i + x:i + x + 3, j + y:j + y + 3] = 1
                            else:
                                if (j % 20 == 0):
                                    pattern[i + x:i + x + 3, j + y + 10:j + y + 13] = 1
                pattern = np.array(pattern[60:1140,80:2000]).reshape((1080,1920))
                f = np.zeros((1080,1920))
                f = pattern
                images.append(f)

        count = 400
        self.dlp.stopsequence()
        self.dlp.changemode(3)
        exposure = [150000] * count
        dark_time = [0] * count
        trigger_in = []
        for i in range(count):
            trigger_in.append(False)

        # trigger_in=[False]*90
        trigger_out = [1] * count
        self.dlp.defsequence(images, exposure, trigger_in, dark_time, trigger_out, 0)

        self.dlp.startsequence()


