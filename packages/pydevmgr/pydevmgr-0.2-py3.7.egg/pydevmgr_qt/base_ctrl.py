from pydantic import BaseModel
from pydevmgr import NodeVar, DataLink, UaDevice, Downloader
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame
from .base import BaseUiLinker, BaseUi, record_widget_factory

from .io import find_ui

class BaseStatData(BaseModel):
    state: NodeVar[int] = 0
    state_txt: NodeVar[str] =  ""
    state_group: NodeVar[int] = 0
    
    substate: NodeVar[int] = 0
    substate_txt: NodeVar[str] = ""
    substate_group: NodeVar[int] = "" 
    
    error_code: NodeVar[int] = 0
    error_txt: NodeVar[str] = ""
    error_group: NodeVar[int] = 0
    
class BaseData(BaseModel):
    stat: BaseStatData = BaseStatData()
    ignored: NodeVar[bool] = False
    name: str = "" # device name  

    
        
class BaseCtrlUi(QFrame, BaseUi):
    def init_ui(self):
        uic.loadUi(find_ui('base_ctrl_frame.ui'), self)      
        
class BaseCtrl(BaseUiLinker):
    Widget = BaseCtrlUi
    Data = BaseData
    
    def init_vars(self):
        # these shall get stat data
        self.outputs.state    = self.outputs.Code(self.widget.state )
        self.outputs.substate = self.outputs.Code(self.widget.substate )
        self.outputs.error    = self.outputs.Code(self.widget.error_txt )
                
        self.outputs.name =  self.outputs.Str(self.widget.name)
        
        self.outputs.rpc_feedback = self.outputs.Feedback(self.widget.rpc_feedback)
        self.inputs.ignored = self.inputs.NBool(self.widget.check)
                    
    def feedback(self, er, msg=''):
        self.outputs.rpc_feedback.set((er, msg))       
        
    def update(self, data : BaseData) -> None:
        """ update the ui from the data structure """
        stat = data.stat
        
        if self._did_failed:
            self.widget.setEnabled(True)
            self._did_failed = False
        
        
                
        self.outputs.state.set( (stat.state, stat.state_txt, stat.state_group) )
        self.outputs.substate.set( (stat.substate, stat.substate_txt, stat.substate_group) ) 
        self.outputs.error.set( (stat.error_code, stat.error_txt, stat.error_group) )
        
        if self.inputs.ignored.get() != data.ignored:             
            self.inputs.ignored.set_input(data.ignored)    
            
        
    def connect_device(self, device, data):   
        super().connect_device(device, data)
                                    
        self.outputs.name.set(data.name or device.key)
        
        self.setup_actions(device, data)
        if hasattr(self.widget, "check"):
            self.setup_ignore_checkbox(device,data)
            
    def setup_ignore_checkbox(self, device, data):
        w = self.widget.check
        w.setChecked(not device.ignored.get())        
        def check_change(state):        
            device.ignored.set(state)
        
        self.actions.add(check_change, [self.inputs.ignored.get]).connect_checkbox(w)
    
    def setup_actions(self, device, data):
        wa = self.widget.state_action
        wa.clear()
        wa.addItem("")
        
        action_list = [
         ("INIT",   device.init,   []), 
         ("ENABLE", device.enable, []),
         ("DISABLE",device.disable,[]),
         ("RESET",  device.reset,  []) 
        ]
        reset = lambda: wa.setCurrentIndex(0)
        
        for i, (name,func,inputs) in  enumerate(action_list, start=wa.count()):
            wa.addItem(name)
            action = self.actions.add(func, inputs, after=reset, feedback=self.feedback)
            action.connect_item(wa, i)
        
record_widget_factory("ctrl", "Device", BaseCtrl)
