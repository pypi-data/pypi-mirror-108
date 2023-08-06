from pydantic import BaseModel
from pydevmgr import NodeVar, DataLink, UaDevice, Downloader
from .tools import STYLE, method_switcher, record_widget, method_setup, get_style, get_widget_constructor
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame
from .base import BaseUi
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

class BaseData(BaseModel):
    stat: BaseStatData = BaseStatData()
    ignored: NodeVar[bool] = False
    name: str = "" # device name  


class BaseCtrl(QFrame, BaseUi):    
    def init_ui(self):
        uic.loadUi(find_ui('base_ctrl_frame.ui'), self)        
    
    def new_data(self, **kwargs) -> BaseData:    
        return BaseData(**kwargs) 
       
    def feedback(self, msgs, er):
        if msgs:
            self.rpc_feedback.setText("; ".join(msgs))
        if er:
            self.rpc_feedback.setText(str(er))
            self.rpc_feedback.setStyleSheet(get_style(STYLE.ERROR))
        else:
            self.rpc_feedback.setStyleSheet(get_style(STYLE.NORMAL))
        
    def update_ui(self, data : BaseData) -> None:
        """ update the ui from the data structure """
        stat = data.stat
        
        if self._did_failed:
            self.setEnabled(True)
            self._did_failed = False
        
        self.rpc_feedback.update()
        
        self.state.setText("{}: {}".format(stat.state, stat.state_txt))
        self.state.setStyleSheet(get_style(stat.state_group))
                
        self.substate.setText("{}: {}".format(stat.substate, stat.substate_txt))
        self.substate.setStyleSheet(get_style(stat.substate_group))
        
        self.error_txt.setText("{}: {}".format(stat.error_code, stat.error_txt))
        self.error_txt.setStyleSheet( get_style(STYLE.ERROR) if stat.error_code else get_style(STYLE.OK) )
        
        if self.check.isChecked() and data.ignored:
            self.check.setChecked(False)
        elif  (not self.check.isChecked()) and (not data.ignored):  
            self.check.setChecked(True)
    
    def unlink_ui(self):
        super().unlink_ui()
        #disconnect all callback event associated to widgets 
        try:            
            self.check.stateChanged.disconnect()
            self.state_action.currentIndexChanged.disconnect()
        except TypeError:
            pass    
        
    def setup_ui(self, device, data, more_methods=[]):   
        super().setup_ui(device, data)                            
        self.name.setText(data.name or device.key)
        self.setup_actions(device, data)
        if hasattr(self, "check"):
            self.setup_ignore_checkbox(device,data)
            
    def setup_ignore_checkbox(self, device, data):
        self.check.setChecked(not device.ignored.get())
        def check_change():
            device.ignored.set( not self.check.isChecked())
        self.check.stateChanged.connect(check_change)    
    
    def list_actions(self, device):
        """ list actions for the combo menu of change state command """
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
        
record_widget("ctrl", "Device", BaseCtrl)    