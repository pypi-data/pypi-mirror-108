from pydantic import BaseModel
from pydevmgr_elt import NodeVar, DataLink, UaDevice, Downloader
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QCheckBox
from .base import BaseUi, BaseUiLinker, record_widget_factory
from .io import find_ui

from enum import Enum 
        
        
class DeviceCfgUi(QFrame, BaseUi):
    def init_ui(self):
        pass
        
class DeviceData(BaseModel):
    name: str = "" # device name  
            
# place holder for some base setup for config pannels 
# not sure we have any             
class DeviceCfg(BaseUiLinker):
    Widget = DeviceCfgUi
    Data = DeviceData
            
record_widget_factory("cfg", "Device", DeviceCfg) 

