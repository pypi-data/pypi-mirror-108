from pydantic import BaseModel
from pydevmgr import NodeVar, DataLink, UaDevice, Downloader
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QCheckBox
from .base import BaseUi, BaseUiLinker, record_widget_factory
from .io import find_ui

from enum import Enum 
        
        
class BaseCfgUi(QFrame, BaseUi):
    def init_ui(self):
        pass
        
class BaseData(BaseModel):
    name: str = "" # device name  
            
# place holder for some base setup for config pannels 
# not sure we have any             
class BaseCfg(BaseUiLinker):
    Widget = BaseCfgUi
    Data = BaseData

            
record_widget_factory("cfg", "Device", BaseCfg) 

