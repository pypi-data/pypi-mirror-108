from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

from pydevmgr_qt.device_ctrl import DeviceCtrl
from pydevmgr_qt.device_line import DeviceLine
from pydevmgr_qt.motor_ctrl import MotorCtrl
from pydevmgr_qt.motor_line import MotorLine
from pydevmgr_qt.motor_cfg import MotorCfg

from pydevmgr_qt.base import get_widget_factory
from pydevmgr_qt.manager import DeviceContainer, DeviceSwitchView


from pydevmgr_elt import Motor, Downloader, open_device, Time


device = None
time = None
counter = 0

def main():
    global device
    device = open_device('tins/motor1.yml', 'motor1')
    device = open_device('tins/adc1.yml', 'adc1')
    #device = open_device('tins/drot1.yml', 'drot1')
    #device = open_device('tins/lamp1.yml', 'lamp1')
    #device = open_device('tins/shutter1.yml', 'shutter1')
    #device = open_device('fsel_motors.yml', 'motor_h')
    
    device.connect();# device.configure()
    downloader = Downloader()
    
    app = QApplication(sys.argv)
    win = QtWidgets.QWidget()
    layout =  QtWidgets.QVBoxLayout(win)
    
    #motFrame1 = DeviceCtrlLink( DeviceCtrl() )
    ctrl = get_widget_factory("ctrl", device.dev_type).build().connect(downloader, device, link_failure=True)
    layout.addWidget(ctrl.widget)
    line = get_widget_factory("line", device.dev_type).build().connect(downloader, device, link_failure=True)
    layout.addWidget(line.widget)
        
    ctrl = DeviceSwitchView().connect(downloader, device, link_failure=True)
    layout.addWidget(ctrl.widget)
    
    
    time  = Time('time', config=Time.Config(address=device.config.address, prefix="MAIN.timer"))
    time.connect()
    ctrl = get_widget_factory("ctrl", time.dev_type).build().connect(downloader, time, link_failure=True)
    layout.addWidget(ctrl.widget)
    
    
    # cfg  = get_widget_factory("cfg", "Motor").build().connect(downloader, device, link_failure=True)
    # layout.addWidget(cfg.widget)
    
    # ctrl = MotorCtrlLink( MotorCtrlUi()).connect( downloader, device, link_failure=True )
    # line = MotorLineLink( MotorLineUi()).connect(downloader,   device, link_failure=True )
    # cfg  = MotorCfgLink( MotorCfgUi()).connect(downloader,    device, link_failure=True )
    
    
    
    
    
    # e_button = QPushButton()
    # e_button.setText("Enable")
    # e_button.clicked.connect(cfg.enable)
    # d_button = QPushButton()
    # d_button.setText("Disable")
    # d_button.clicked.connect(cfg.disable)
    # layout.addWidget(e_button)
    # layout.addWidget(d_button)
    # 
    # def toto(dummy=None):
    #     global counter
    # 
    #     print(counter, len(downloader.data))
    #     if counter>20:
    #         cfg.disable()
    #         downloader.data.clear()
    #     if counter>40:
    #         cfg.enable()
    #         downloader.data.clear()
    #     counter += 1
    #downloader.add_callback(..., toto)
    #cfg.disable()
    #cfg.enable()
    
    win.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    timer.start(100)
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    try:
        main()
    finally:
        if device:
            device.disconnect()
        if time:
            time.disconnect()