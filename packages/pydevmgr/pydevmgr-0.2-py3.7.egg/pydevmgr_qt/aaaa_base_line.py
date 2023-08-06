from pydantic import BaseModel
from pydevmgr import NodeVar, DataLink, UaDevice, Downloader
from .tools import STYLE, method_switcher, record_widget, method_setup, get_style, get_widget_constructor
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame
from .base import BaseUi
from .io import find_ui

class BaseStatData(BaseModel):
    substate: NodeVar[int] = 0
    substate_txt: NodeVar[str] = ""
    substate_group: NodeVar[int] = "" 

class BaseData(BaseModel):
    stat: BaseStatData = BaseStatData()
    ignored: NodeVar[bool] = False
    name: str = "" # device name  


class BaseLine(QFrame, BaseUi):
    
    def init_ui(self):
        uic.loadUi(find_ui('base_line_frame.ui'), self)
    
    def new_data(self, **kwargs) -> BaseData:    
        return BaseData(**kwargs) 
     
    def feedback(self, msgs, er):
        if er:
            #self.state_action.setStyleSheet("border-color: red;")
            self.state_action.setItemText(0, '!ERROR')
        else:
            self.state_action.setItemText(0, '')
            #self.state_action.setStyleSheet(STYLE.NORMAL)
            
    def update_ui(self, data):        
        if self._did_failed:
            self.setEnabled(True)
            self._did_failed = False
                
        self.substate.setText("{}".format(data.stat.substate_txt))
        self.substate.setStyleSheet(get_style(data.stat.substate_group))
        
        if self.check.isChecked() and data.ignored:
            self.check.setChecked(False)
        elif  (not self.check.isChecked()) and (not data.ignored):  
            self.check.setChecked(True)
            
    def unlink_ui(self):
        super().unlink_ui()        
        try:            
            self.check.stateChanged.disconnect()
            self.state_action.currentIndexChanged.disconnect()
        except TypeError:
            pass    
    
    
    def setup_ui(self, device, data): 
        super().setup_ui(device, data)
        
        self.name.setText( data.name or device.key )   
        self.setup_actions(device, data)        
        if hasattr(self, "check"):
            self.setup_ignore_checkbox(device,data)
    
    def list_actions(self, device):
        return [
           ("",       None,          []), 
           ("INIT",   device.init,   []), 
           ("ENABLE", device.enable, []),
           ("DISABLE",device.disable,[]),
           ("RESET",  device.reset,  []) 
        ]
    
    def setup_actions(self, device, data):        
        actions = self.list_actions(device)
                
        # action menu 
        self.state_action.clear()
        # Add items to combo and remove string "---" separator from stat_methods
        actions = method_setup(self.state_action, actions)
                    
        func = method_switcher(actions, self.feedback, 
                                       lambda : self.state_action.setCurrentIndex(0)
                                       )
        self.state_action.currentIndexChanged.connect(func)                        
    
    def setup_ignore_checkbox(self, device, data):
        self.check.setChecked(not device.ignored.get())
        def check_change():
            device.ignored.set( not self.check.isChecked())
        self.check.stateChanged.connect(check_change)

record_widget("line", "Device", BaseLine)  