from PyQt5.QtWidgets import QAction, qApp, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QFrame, QCheckBox, QComboBox, QLabel, QMenu, QMainWindow
from PyQt5 import uic 
from .base import BaseUiLinker, BaseUi, WidgetControl, get_widget_factory

from pydevmgr_qt.io import find_ui

#from pydevmgr_qt.tools import  Actions, get_style
from pydevmgr_elt import NodeVar, Downloader, UaManager

from typing import Union, Iterable, Optional, List, Tuple, Dict

from pydantic import BaseModel, validator
from .device_widget import default_layouts, DeviceLayout
import os

class ManagerStatData(BaseModel):
    state: NodeVar[int] = 0
    state_txt: NodeVar[str] = ""
    state_group: NodeVar[str] = ""

class ManagerCtrlData(BaseModel):
    stat: ManagerStatData = ManagerStatData()
    
class ManagerData(BaseModel):
    StatData = ManagerStatData 
    
    stat: ManagerStatData = ManagerStatData()
    name : str = ""
    layout_name: Optional[str] = None # layout name (one of the layouts dictionary) if None take the first one
    layouts: Optional[Dict[str,DeviceLayout]] = None    # A dictionary defining all the available device layouts for manager 
                                      # if None, default is used 
    curent_layout: Optional[DeviceLayout] = None # The curent layout by default the first of layouts of the dict



def get_layout_def(manager: UaManager, name: str) -> Tuple: 
    """ Return the definition of a layout from its name inside a manager """   
    all_layouts_def = manager_layouts(manager)
    # if None, take the first one                                      
    if name is None:
        name = next(all_layouts_def.__iter__())
    layout_def = all_layouts_def[name]    
    return name, DeviceLayout.parse_obj(layout_def)

def manager_layouts(manager:  UaManager) -> dict:
    """ Dictionary containing all layout associated to this manger or defaults """
    try:
        all_layouts_def = manager.extra['layouts']
    except KeyError:
        all_layouts_def = default_layouts
    else:
        if not all_layouts_def:
            all_layouts_def = default_layouts
    return all_layouts_def

def set_layout_to_data(manager: UaManager, data: ManagerData) -> None:    
    """ Change the current_layout to data structur according to the layouts dictionary and layout_name 
    
    If data.layouts is None it is loaded from the extra of the manager or a default one is loaded 
    If data.layout_name is None, the first layout of data.layouts is taken
    If data.curent_layout is None it is replaced by data.layouts[data.layout_name]
    """
    if data.layouts is None:
        data.layouts = manager_layouts(manager)    
    if data.layout_name is None:
        data.layout_name = next(data.layouts.__iter__())
    if data.curent_layout is None:                
        data.curent_layout  = DeviceLayout.parse_obj(data.layouts[data.layout_name])

    
class ManagerStateUi(BaseUi, QWidget):
    """ A very small widget with manager state """    
    def init_ui(self):
        layout = QGridLayout(self)
        
        self.state = QLabel()
        self.state.setMaximumWidth(300)
        
        layout.addWidget(self.state, 0, 0)
        self.layout = layout
        
class ManagerState(BaseUiLinker):
    Widget = ManagerStateUi
    Data = ManagerData
    def init_vars(self):
        self.state = self.outputs.Code(self.widget.state)
        
    def update(self,data):
        stat = data.stat
        self.state.set( (stat.state, stat.state_txt, stat.state_group) ) 
    

class ManagerDevicesUi(BaseUi, QWidget):
    """ Act as a container for device layout """    
    def init_ui(self):
        layout = QGridLayout(self)
        self.layout = layout


class ManagerDevicesLinker(BaseUiLinker):
    """ This is the widget linker for a pannel with devices 
    
    The layout is defined inside the data.
    """
    Widget = ManagerDevicesUi
    Data = ManagerData
    
    container_widget = None
    device_and_linkers = None
    widget_controls = None
    
    def connect(self, 
          downloader: Downloader, 
          manager: UaManager,
          data = None,  
          link_failure: bool = False, 
          link_update: bool = True
        ) -> WidgetControl:
        if data is None:
            data = self.Data()
        ctrl = super().connect(downloader, manager, data, link_failure=link_failure, link_update=link_update)
        
        self.widget_controls = []
        for device,linker in self.device_and_linkers:            
            self.widget_controls.append( linker.connect(downloader,device, link_update=link_update) )
            
        return ctrl 
            
            
    def disconnect(self):
        super().disconnect()
        if self.widget_controls:
            for ctrl in self.widget_controls:
                ctrl.kill()
        self.widget_controls = None
        # remove 
        # if self.container_widget is not None:
        #     self.container_widget.setParent(None)
        self.device_and_linkers = None
        if self.container_widget:
            self.container_widget.setParent(None)
        
    def connect_device(self, manager, data):
        super().connect_device(manager, data)
                
        set_layout_to_data(manager, data)
        
        self.container_widget, self.device_and_linkers = data.curent_layout.insert_widgets(manager)        
        self.widget.layout.addWidget(self.container_widget)
        

class ManagerMainUi(QMainWindow, BaseUi):
    views=None
    def init_ui(self):
        
        self.devices = ManagerDevicesLinker.Widget()
        self.state = ManagerState.Widget()
        
        main = QWidget()
        vlayout = QVBoxLayout(main)
        
        vlayout.addWidget(self.state)
        vlayout.addWidget(self.devices)
        
        self.setCentralWidget(main)
        self.statusBar().showMessage('Ready')
        
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        
        self.resize(750, 1000)
                
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        
        fileMenu.addAction(exitAct)
        
        self.viewMenu = QMenu("&View", self)
        menuBar.addMenu(self.viewMenu)
        
        self.actionMenu = QMenu("&Action", self)
        menuBar.addMenu(self.actionMenu)
        
class ManagerMain(BaseUiLinker):
    Widget =  ManagerMainUi
    Data = ManagerData
    
    devices = None
    state = None
    
    def feedback(self, er, msg):
        pass
    
    # def update(self, data):
    #     super().update(data)
    # 
    #     self.state.update(data)
    #     self.devices.update(data)
    
    def connect(self, downloader, manager, data=None, *args, **kwargs):
        ctrl = super().connect(downloader, manager, data, *args, **kwargs)
        
        if data is None:
            data = self.Data()
        self.devices = ManagerDevicesLinker(self.widget.devices)
        
        self.devices.connect( downloader, manager, data, link_update = True)
        
        self.state = ManagerState(self.widget.state)
        
        self.state.connect( downloader, manager, data, link_update = True)
        
        
        def view_changed(layout_name):
            data.layout_name = layout_name   
            data.curent_layout = None # will be replaced according to name by self.devices.connect
            
            self.devices.disconnect()
            self.devices.connect( downloader, manager, data )
            
        for layout_name, layout_def in data.layouts.items():
            viewAct = QAction(layout_name, self.widget)
            self.widget.viewMenu.addAction(viewAct)
            self.actions.add(view_changed, [layout_name]).connect_action(viewAct)
            
        return ctrl   
    
    def disconnect(self):
        if self.devices:
            self.devices.disconnect()   
        if self.state:
            self.state.disconnect() 
        super().disconnect()
    
    def connect_device(self, manager, data):
        
        action_list = [
         ("INIT",   manager.init,   []), 
         ("ENABLE", manager.enable, []),
         ("DISABLE",manager.disable,[]),
         ("RESET",  manager.reset,  []), 
         ("---",  None,  []),
         ("CONFIGURE", manager.configure, []),
         ("---",  None,  []),
         ("CHECK ALL", manager.unignore_all, []),
         ("UNCHECK ALL", manager.ignore_all, []),
        ]
        for name,func,inputs in action_list:
            if name == "---":
                self.widget.actionMenu.addSeparator()
                continue
            act = QAction(name, self.widget)
            self.widget.actionMenu.addAction(act)
            self.actions.add(func, inputs, feedback=self.feedback).connect_action(act)
        

class DeviceSwitchData(BaseModel):
    widget_type : str = "line"        
    widget_types : List[str] = ["line", "ctrl", "cfg"]
    

class DeviceContainerUi(BaseUi, QWidget):
    def init_ui(self):
        #self.container = QWidget()
        self.layout = QVBoxLayout(self)
        #self.layout.addWidget(self.container)
    
class DeviceContainer(BaseUiLinker):
    Data = DeviceSwitchData
    Widget = DeviceContainerUi
    linker = None
    _change_view = None
    def connect(self, downloader, device, data=None, link_failure=False, link_update=True):
        if data is None:
            data = self.Data()
        
        def change_view(view): 
            data.widget_type = view  
                     
            if self.linker:
                self.linker.widget.setParent(None)
                self.linker.disconnect()
                        
            self.linker = get_widget_factory(data.widget_type, device.dev_type).build()
            self.linker.connect(downloader, device)
                        
            self.widget.layout.addWidget(self.linker.widget)
        
        self._change_view = change_view
        
        for view in data.widget_types:
            try:
                get_widget_factory(view, device.dev_type)
            except (KeyError, ValueError):
                continue
            change_view(view)
            break
        
        
        return super().connect(downloader, device, data, link_failure= link_failure, link_update=link_update)
        
    def change_view(self, view):
        if self._change_view:
            self._change_view(view)
    
    
    
    
        
    def disconnect(self):
        super().disconnect()
        if self.linker:
            self.linker.disconnect()
        self.linker.widget.setParent(None)
        
    
                    
        
        
class DeviceSwitchViewUi(BaseUi, QWidget):
    def init_ui(self):
        layout = QHBoxLayout(self)
        self.switcher = QComboBox()
        self.container = QWidget()
        layout.addWidget(self.switcher)
        layout.addWidget(self.container)
        self.layout = layout
    
        

class DeviceSwitchView(BaseUiLinker):
    Widget = DeviceSwitchViewUi
    Data = DeviceSwitchData
    
    container_linker = None    
    device = None
    
    def connect(self, downloader, device, data=None, link_failure=False, link_update=True):
        if data is None:
            data = self.Data()
                    
        self.device = device
        if self.container_linker:
            self.container_linker.disconnect()
        
        self.container_linker = DeviceContainer()                    
        self.container_linker.connect(downloader, device, data)
        
        # remove the widget and replace it by a new one 
        self.widget.container.setParent(None)
        self.widget.container = self.container_linker.widget
        self.widget.layout.addWidget(self.widget.container)
        ctrl = super().connect(downloader, device, data, link_failure=link_failure, link_update=link_update)
        
        
        self.widget.switcher.clear()
        for view in data.widget_types:
            try:
                get_widget_factory(view, device.dev_type)
            except (KeyError, ValueError):
                continue
            self.widget.switcher.addItem(view)
            self.actions.add(self.container_linker.change_view, [view]).connect_item(self.widget.switcher, self.widget.switcher.count()-1)
            if view == data.widget_type:
                self.widget.switcher.setCurrentIndex( self.widget.switcher.count()-1 )                            
                
        return ctrl 
            
    def change_view(self, view):
        pass     
        
        
        
        
        

        