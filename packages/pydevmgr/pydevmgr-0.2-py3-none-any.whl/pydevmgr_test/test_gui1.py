from pydevmgr_qt.motor_ctrl import MotorCtrl
from pydevmgr_qt.motor_line import MotorLine
from pydevmgr_qt.motor_cfg import MotorCfg

from pydevmgr_qt.adc_ctrl import AdcCtrl
from pydevmgr_qt.adc_line import AdcLine

from pydevmgr_qt.drot_ctrl import DrotCtrl
from pydevmgr_qt.drot_line import DrotLine

from pydevmgr_qt.lamp_ctrl import LampCtrl
from pydevmgr_qt.lamp_line import LampLine

from pydevmgr_qt.shutter_ctrl import ShutterCtrl
from pydevmgr_qt.shutter_line import ShutterLine
from pydevmgr_qt.device_ctrl import DeviceCtrl
from pydevmgr_qt.device_line import DeviceLine 

from pydevmgr_elt import open_device, Downloader
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


if __name__ =="__main__":

    app = QApplication(sys.argv)
    #win = MotorCtrl()
    win = MotorCfg()
    dev = open_device('tins/motor1.yml', 'motor1')
    #dev = open_device('tins/adc1.yml')
    downloader = Downloader()
    
    win.link_and_setup_ui(downloader, dev)
        
    win.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    timer.start(200)
    c = 9
    try:
        dev.connect()
        c = app.exec_()
    finally:
        dev.disconnect()
        sys.exit(c)
  