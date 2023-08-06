from pydantic import BaseModel
from pydevmgr_elt import NodeVar, DataLink, UaDevice, Downloader, CcsSim
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame
from .base import BaseUiLinker, BaseUi, record_widget_factory

from .io import find_ui
import datetime 


def now():
    return datetime.datetime.utcnow().isoformat().replace("T", "-") 


class CcsSimStatData(BaseModel):
        
    time: NodeVar[str] = ""
    mode_txt: NodeVar[str] = ""
    error_msg: NodeVar[str] = ""
    
    
class CcsSimData(BaseModel):
    StatData = CcsSimStatData # save StatData class here 
    
    stat: StatData = StatData()    
    name: str = "CcsSim" 
    
        
class CcsSimCtrlUi(QFrame, BaseUi):
    def init_ui(self):
        uic.loadUi(find_ui('time_ctrl_frame.ui'), self)      
        
class CcsSimCtrl(BaseUiLinker):
    Widget = CcsSimCtrlUi
    Data = CcsSimData
    
    def init_vars(self):
        # these shall get stat data
        self.outputs.time = self.outputs.Str(self.widget.time)
        self.outputs.mode    = self.outputs.Str(self.widget.mode)
        self.outputs.rpc_feedback = self.outputs.Feedback(self.widget.rpc_feedback)
        self.outputs.error    = self.outputs.Str(self.widget.error)
        
        self.inputs.time = self.inputs.Str(self.widget.in_time)
            
    def feedback(self, er, msg=''):
        self.outputs.rpc_feedback.set((er, msg))              
    
    def update(self, data : CcsSimData) -> None:
        """ update the ui from the data structure """
        super().update(data)
        stat = data.stat
                                        
        #self.outputs.dc_time.set( stat.dc_time  )
         
        self.outputs.time.set( stat.time ) 
        self.outputs.mode.set(  stat.mode_txt )
        self.outputs.error.set( stat.error_msg)
        
        
    def connect_device(self, device, data):   
        super().connect_device(device, data)
                                    
        #self.outputs.name.set(data.name or device.key)
        
        
        def now():
            self.widget.in_time.repaint()
            return datetime.datetime.utcnow().isoformat().replace("T", "-") 
            
        def simulate(time):
            #self.set_mode(device.MODE.LOCAL) # to Clear any error ! 
            self.outputs.error.set("") # because this is not cleared on the PLC side 
            self.widget.error.repaint()
            device.set_time(time)
            
        
        self.actions.add(
               simulate,
               [self.inputs.time.get], feedback=self.feedback
               ).connect_button(self.widget.set_simulate)
        self.actions.add(
               device.set_mode,
               [CcsSim.MODE.LOCAL], feedback=self.feedback
               ).connect_button(self.widget.set_local_mode)
        self.actions.add(
               device.set_mode,
               [CcsSim.MODE.UTC], feedback=self.feedback
               ).connect_button(self.widget.set_utc_mode)
        self.actions.add(
                self.inputs.time.set_input, 
                [now], feedback=self.feedback
               ).connect_button(self.widget.set_now)
        
record_widget_factory("ctrl", "CcsSim", CcsSimCtrl)
