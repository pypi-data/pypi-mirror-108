from PyQt5 import  uic
from .io import find_ui
from .device_line import  record_widget_factory, DeviceLine, DeviceLineUi 


class ShutterLineUi(DeviceLineUi):
    def init_ui(self):
        uic.loadUi(find_ui('shutter_line_frame.ui'), self)

class ShutterLine(DeviceLine):
    Widget = ShutterLineUi
    
    def connect_device(self, shutter, data):        
        super().connect_device(shutter, data)
        wa = self.widget.state_action
        # After an command put back the menu to the empty first index
        reset = lambda : wa.setCurrentIndex(0)
        wa.insertSeparator(wa.count())
        
        wa.addItem("OPEN")
        self.actions.add( shutter.open, 
                         after=reset, feedback=self.feedback,
                         ).connect_item(wa, wa.count()-1)
        
        wa.addItem("CLOSE")
        self.actions.add( shutter.close, 
                         after=reset, feedback=self.feedback,
                         ).connect_item(wa, wa.count()-1)
                         
record_widget_factory("line", "Shutter", ShutterLine)