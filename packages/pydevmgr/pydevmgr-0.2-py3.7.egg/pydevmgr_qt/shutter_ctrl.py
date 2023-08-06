from PyQt5 import  uic
from .io import find_ui
from .device_ctrl import  record_widget_factory, DeviceCtrl, DeviceCtrlUi


class ShutterCtrlUi(DeviceCtrlUi):
    def init_ui(self):
        uic.loadUi(find_ui('shutter_ctrl_frame.ui'), self)

class ShutterCtrl(DeviceCtrl):
    Widget = ShutterCtrlUi                  
    
    def connect_device(self, shutter, data):        
        super().connect_device(shutter, data)
                
        # link the buttons to an action
        self.actions.add(shutter.open, feedback=self.feedback).connect_button(self.widget.open)
        self.actions.add(shutter.close, feedback=self.feedback).connect_button(self.widget.close)        

record_widget_factory("ctrl", "Shutter", ShutterCtrl)