""" Tools to link a widget and a device or a set of widget-device """
from pydantic import BaseModel, validator
from typing import Optional, Dict , Union, Iterable, List
from PyQt5.QtWidgets import QLayout, QBoxLayout, QGridLayout, QWidget
from PyQt5.uic import loadUi
from pydevmgr_elt import UaDevice, UaManager
from .base import get_widget_factory
from PyQt5 import QtCore
from .io import find_ui, load_config
from warnings import warn 
import glob 

## ###############################################################
##    DeviceWidget  :  Tools to link device with Widget in Layout 
##      This is mostly used for automatic creation of device widgets 
## ###############################################################

class DeviceWidgetSetup(BaseModel):
    """ Use to define the creation of a widget inside a QLayout 
    
    All argument are optional except ``layout`` 
    
    Args:
       - layout (str): layout name found in the ui 
       - device (str,list):  add widget  of matching name device can be a glob to match (e.g. motor[1-4])
                        This can be also a list of strict names 
       - dev_type (str,list): add widget matching the given device type ('Any' will match all devices) (e.g. Motor)
                        This can be also a list of strict type
       - exclude_device (str,list): work as `device` but for exclusion 
       - exclude_dev_type (str,list): work as `dev_type` but for exclusion 
       - widget_kind (str):  The widget kind  "line", "ctrl", "cfg"
       - widget_class (str): Can be use if a device has no widget defined one can use the widget of an other type 
       - alt_layout (str,Iterable): If layout is not found try with the alternative ones 
       
       - column (int):  default, 0. Used only if the layout is a QGridLayout 
       - row (int): default, 0. Used only if the layout is a QGridLayout 
       - columnSpan (int): default, 1. Used only if the layout is a QGridLayout 
       - rowSpan (int):  default, 1. Used only if the layout is a QGridLayout 
       
       - stretch (int):  default, 0. Used only if the layout is a QBoxLayout
       - alignment (int): default, 0. Used only if the layout is a QBoxLayout see PyQt5 doc           
    """
    layout: str = "ly_devices" 
    device: Union[str, Iterable] = "*"
    dev_type: Union[str, Iterable]  = "*"
    
    exclude_device: Union[str, Iterable] = ""
    exclude_dev_type: Union[str, Iterable]  = ""
    
    widget_kind: str = "ctrl"
    widget_class: Optional[str] = None
    alt_layout: Union[str,Iterable] = []
    column: int = 0
    row: int = 0
    columnSpan: int = 1
    rowSpan: int = 1
    
    stretch: int = 0
    alignment: int = 0 
    
    class Config:
        extra = 'forbid'
    
    @validator("alt_layout")
    def _liste_me(cls, value):
        return [value] if isinstance(value, str) else value

    def find_devices(self, manager: Union[UaManager, UaDevice]) -> List[UaDevice]:
        """ Collect devices from the manager according to matching rules 
        
        The mathcing rules are defined by the properties :
        
        - device: Union[str, Iterable] = "*"
        - dev_type: Union[str, Iterable]  = "*"        
        - exclude_device: Union[str, Iterable] = ""
        - exclude_dev_type: Union[str, Iterable]  = ""
        
        Returns:
           devices: list of matching devices
        """
        
        devices = []
        match_device = _obj_to_match_func(self.device)
        match_type   = _obj_to_match_func(self.dev_type)
        
        exclude_match_device = _obj_to_match_func(self.exclude_device)
        exclude_match_type   = _obj_to_match_func(self.exclude_dev_type)
        for device in manager.devices():        
            if exclude_match_device(device.name): continue
            if exclude_match_type(device.dev_type): continue
            if match_device(device.name) and match_type(device.dev_type):
                devices.append(device)  
        return devices
    
    def find_layout(self, ui: QWidget) -> QLayout:
        """ find a layout from a parent ui according to config 
        
        Look for a layout named as .layout properties. If not found look inside 
        the .alt_layout list property. 
        """
        layout = ui.findChild(QLayout, self.layout)
        if layout is None:
            for ly_name in self.alt_layout:
                layout = ui.findChild(QLayout, ly_name)
                if layout: break
            else:
                raise ValueError(f"Cannot find layout with the name {self.name!r} or any alternatives")
        return layout
    
    def insert_widgets(self, 
          manager: UaManager, 
          ui: QWidget
        ) -> list:
        devices = self.find_devices(manager)
        layout = self.find_layout(ui)
        
        device_linker = []
        default_factory = get_widget_factory(self.widget_kind, 'Device')
        
        for device in devices:
            factory = get_widget_factory(self.widget_kind, device.dev_type, default=default_factory)   
            
            linker = factory.build()
            widget = linker.widget 
            if isinstance(layout, QBoxLayout): 
                layout.addWidget(widget, self.stretch, QtCore.Qt.AlignmentFlag(self.alignment))
            elif isinstance(layout, QGridLayout):
                layout.addWidget(widget, self.row, self.column, self.rowSpan, self.columnSpan)
            else:
                layout.addWidget(widget)  
            device_linker.append( (device, linker) )
        
        return device_linker  
        

class DeviceLayout(BaseModel):
    """ One item that define a layout compose from a ui resource file and a setup """
    ui_file: str = "simple_devices_frame.ui"
    setup: List[DeviceWidgetSetup] =  DeviceWidgetSetup(device="*", layout="ly_devices", widget_kind="ctrl")
    size: Optional[List] = None
    
    @validator("ui_file")
    def _validate_ui_file(cls, ui_file):
        """ Check if ui_file exists in resources """
        try:
            find_ui(ui_file) 
        except IOError as e:
            raise ValueError(e)
        return ui_file
        
    def insert_widgets(self, 
          manager: UaManager, 
          ui: QWidget = None
        ) -> list:
        if ui is None:
            ui = loadUi(find_ui(self.ui_file))
            
        device_linker = []
        for setup in self.setup:
            device_linker.extend( setup.insert_widgets(manager, ui) )
        return ui, device_linker


default_layouts = {
          "line":DeviceLayout(setup=[DeviceWidgetSetup(device="*", layout="ly_devices", widget_kind="line")]),
          "ctrl":DeviceLayout(setup=[DeviceWidgetSetup(device="*", layout="ly_devices", widget_kind="ctrl")])
        }
        
class DeviceLayouts(BaseModel):    
    __root__: Dict[str,DeviceLayout] = default_layouts


def _obj_to_match_func(obj):
    if not obj:
        return lambda name: False 
    if isinstance(obj, str):
        return lambda name: glob.fnmatch.fnmatch(name, obj)
    elif hasattr(obj, "__iter__"): 
        return  lambda name: name in obj


