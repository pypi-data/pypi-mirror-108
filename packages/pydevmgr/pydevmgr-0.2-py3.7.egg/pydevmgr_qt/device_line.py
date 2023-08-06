from pydantic import BaseModel
from pydevmgr_elt import NodeVar, UaDevice

from PyQt5 import uic
from PyQt5.QtWidgets import QFrame
from .base import BaseUi, BaseUiLinker, record_widget_factory

from .io import find_ui

class DeviceStatData(BaseModel):
    substate: NodeVar[int] = 0
    substate_txt: NodeVar[str] = ""
    substate_group: NodeVar[int] = "" 

class DeviceData(BaseModel):
    StatData = DeviceStatData
    
    stat: StatData = StatData()
    ignored: NodeVar[bool] = False
    name: str = "" # device name  

class DeviceLineUi(QFrame, BaseUi):
    def init_ui(self):
        uic.loadUi(find_ui('device_line_frame.ui'), self)      

class DeviceLine(BaseUiLinker):  
    Widget = DeviceLineUi
    Data = DeviceData
    def init_vars(self):        
        # these shall get stat data        
        self.outputs.substate = self.outputs.Code(self.widget.substate)
        self.outputs.name = self.outputs.Str(self.widget.name)
        
        self.inputs.ignored = self.inputs.NBool(self.widget.check)
        
    def feedback(self, er, mgs: str=''):     
           
        if er:
            self.widget.state_action.setItemText(0, "!!ERROR!!")
        else:
            self.widget.state_action.setItemText(0, "")    
        
    def update(self, data: DeviceData):        
        
        stat = data.stat 
        self.outputs.substate.set( (stat.substate, stat.substate_txt, stat.substate_group) )
        
        if self.inputs.ignored.get() != data.ignored:
            self.inputs.ignored.set_input(data.ignored)
    
    def connect_device(self, device: UaDevice, data: DeviceData): 
        super().connect_device(device, data)
        
        # The device name is updated here only 
        self.outputs.name.set( data.name or device.key )
        
        # setup the dorpdown menu list for action     
        wa = self.widget.state_action 
        wa.clear() 
        wa.addItem("") # First item is empty and is always activated after an action 
        action_list = [
         ("INIT",   device.init,   []), 
         ("ENABLE", device.enable, []),
         ("DISABLE",device.disable,[]),
         ("RESET",  device.reset,  []) 
        ]
        # After an command put back the menu to the empty first index
        reset = lambda: wa.setCurrentIndex(0) 
                        
        for i, (name,func,inputs) in  enumerate(action_list, start=wa.count()):
            wa.addItem(name)
            action = self.actions.add(func, inputs, after=reset, feedback=self.feedback)
            action.connect_item(wa, i)
        
                
        w = self.widget.check
        w.setChecked(not device.ignored.get())        
                
        self.actions.add(device.ignored.set, [self.inputs.ignored.get], feedback=self.feedback).connect_checkbox(w)
        
record_widget_factory("line", "Device", DeviceLine)  