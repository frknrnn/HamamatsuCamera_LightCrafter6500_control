import nidaqmx
import numpy as np
from nidaqmx import *
import time
import serial
from serial.tools import list_ports

from PySide2.QtCore import *
class piezo(QThread):
    change_pixmap_signal = Signal(list)
    piezoFlag = True

    def connectNI(self):
        ######## Z Stage
        self.task_zw = nidaqmx.Task()
        self.task_zw.ao_channels.add_ao_voltage_chan('Dev1/ao0', "mychannel1", 0, 10)
        self.task_zw.start()

        self.task_input = nidaqmx.Task()
        self.task_input.ai_channels.add_ai_voltage_chan('Dev1/ai0:2', "mychannel1",max_val=10.0,min_val=0.0)
        self.task_input.start()
        self.z_pos = 0
        self.task_zw.write(self.z_pos)

        ############ X Stage
        self.task_xw = nidaqmx.Task()
        self.task_xw.ao_channels.add_ao_voltage_chan('Dev1/ao1', "mychannel2", 0, 10)
        self.task_xw.start()
        self.x_pos = 0
        self.task_xw.write(self.x_pos)

        ########### Y Stage
        self.task_yw = nidaqmx.Task()
        self.task_yw.ao_channels.add_ao_voltage_chan('Dev1/ao2', "mychannel3", 0, 10)
        self.task_yw.start()
        self.y_pos = 0
        self.task_yw.write(self.y_pos)


########## Z Stage Functions #############
    def goZp(self,stepSize):
        self.ZstepSize = stepSize
        self.Zp_timer = QTimer()
        self.Zp_timer.timeout.connect(self.moveZp)
        self.Zp_timer.start(20)

    def moveZp(self):
        if (self.z_pos <= 10):
            self.z_pos = self.z_pos + self.ZstepSize
        self.task_zw.write(self.z_pos)

    def holdZp(self):
        self.Zp_timer.stop()

    def goZn(self, stepSize):
        self.ZstepSize = stepSize
        self.Zn_timer = QTimer()
        self.Zn_timer.timeout.connect(self.moveZn)
        self.Zn_timer.start(20)

    def moveZn(self):
        if (self.z_pos >= 0):
            self.z_pos = self.z_pos - self.ZstepSize
        self.task_zw.write(self.z_pos)

    def holdZn(self):
        self.Zn_timer.stop()

########### X Stage Functions##############

    def goXp(self, stepSize):
        self.XstepSize = stepSize
        self.Xp_timer = QTimer()
        self.Xp_timer.timeout.connect(self.moveXp)
        self.Xp_timer.start(20)

    def moveXp(self):
        if (self.x_pos <= 10):
            self.x_pos = self.x_pos + self.XstepSize
        self.task_xw.write(self.x_pos)

    def holdXp(self):
        self.Xp_timer.stop()

    def goXn(self, stepSize):
        self.XstepSize = stepSize
        self.Xn_timer = QTimer()
        self.Xn_timer.timeout.connect(self.moveXn)
        self.Xn_timer.start(20)

    def moveXn(self):
        if (self.x_pos >= 0):
            self.x_pos = self.x_pos - self.XstepSize
        self.task_xw.write(self.x_pos)

    def holdXn(self):
        self.Xn_timer.stop()

########### Y Stage Functions##############

    def goYp(self, stepSize):
        self.YstepSize = stepSize
        self.Yp_timer = QTimer()
        self.Yp_timer.timeout.connect(self.moveYp)
        self.Yp_timer.start(20)

    def moveYp(self):
        if (self.y_pos <= 10):
            self.y_pos = self.y_pos + self.YstepSize
        self.task_yw.write(self.y_pos)

    def holdYp(self):
        self.Yp_timer.stop()

    def goYn(self, stepSize):
        self.YstepSize = stepSize
        self.Yn_timer = QTimer()
        self.Yn_timer.timeout.connect(self.moveYn)
        self.Yn_timer.start(20)

    def moveYn(self):
        if (self.y_pos >= 0):
            self.y_pos = self.y_pos - self.YstepSize
        self.task_yw.write(self.y_pos)

    def holdYn(self):
        self.Yn_timer.stop()




    def focusControl(self,value):
        if(value>0 and value<10):
            self.task_zw.write(value)
            self.z_pos=value



    def run(self):
        while self.piezoFlag:
            pos_list=[]
            result = self.task_input.read()

            x=result[1]
            x_ = round((x * 60) / 100000, 6)
            x_result = round(x_, 5)
            pos_list.append(x_result)

            y = result[2]
            y_ = round((y * 60) / 100000, 6)
            y_result = round(y_, 5)
            pos_list.append(y_result)

            z = result[0]
            z_=round((z*60)/100000,6)
            z_result = round(z_, 5)
            pos_list.append(z_result)


            self.change_pixmap_signal.emit(pos_list)



    def terminate(self):
        self.piezoFlag = False
