from PyQt5.QtWidgets import QAction, qApp, QHBoxLayout, QGridLayout, QWidget, QFrame, QCheckBox, QComboBox, QLabel, QMenu, QMainWindow
from PyQt5 import uic 
from .base import BaseUi

from pydevmgr_qt.io import find_ui
from pydevmgr.base.io import load_config

from pydevmgr_qt.tools import  Actions, get_style
from pydevmgr_qt.device_widget import  get_layout, device_layouts
from pydevmgr import NodeVar
from typing import Union, Iterable, Optional, List
from pydantic import BaseModel, validator
import os

class ManagerStatData(BaseModel):
    state: NodeVar[int] = 0
    state_txt: NodeVar[str] = ""
    state_group: NodeVar[str] = ""

class ManagerCtrlData(BaseModel):
    stat: ManagerStatData = ManagerStatData()

class ManagerData(BaseModel):
    stat: ManagerStatData = ManagerStatData()
    name : str = ""
    layout_name: Optional[str] = None # layout name (as named in extra) if None take the first one
    
    
class ManagerCtrl(QWidget, BaseUi):
    """ Simple Widget for manager allowing to control state and do some action to devices """
    def init_ui(self):
        # only build the Widgets and layout
        # These widget are filled and connected by .setup_ui
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.check_all = QCheckBox()
        self.check_all.setChecked(True)
        self.state_action = QComboBox()
        self.state = QLabel()
        
        layout.addWidget(self.check_all)
        layout.addWidget(self.state_action)
        layout.addWidget(self.state)
    
    def new_data(self,**kwargs):
        return ManagerCtrlData(**kwargs)
    
    def setup_ui(self, manager, data):
        super().setup_ui(manager, data)
        self.state_action.clear()
        action = Actions(
           [
               ("",       None,          []), 
               ("INIT",    manager.init,   []), 
               ("ENABLE",  manager.enable, []),
               ("DISABLE", manager.disable,[]),
               ("RESET",   manager.reset,  []) 
           ] 
        )
        action.connect_combo(self.state_action, reset=lambda : self.state_action.setCurrentIndex(0))
        
        self.state.setText("UNKNOWN")
        
        def check_all():
            c = not self.check_all.isChecked()
            for d in manager.devices():
                d.ignored.set(c)
        self.check_all.stateChanged.connect(check_all)
    
    def disconnect_events(self):
        try:
            self.check_all.stateChanged.disconnect()
            self.state_action.currentIndexChanged.disconnect()    
        except TypeError:
            pass
        
    def update_ui(self, data):
        super().update_ui(data)
        stat = data.stat
        self.state.setText("{}: {}".format(stat.state, stat.state_txt))
        self.state.setStyleSheet(get_style(stat.state_group))
        

            

class ManagerDevices(QFrame, BaseUi):
    
    def new_data(self,**kwargs):
        return ManagerData(**kwargs)
    
    def init_ui(self):
        # this is done in setup when data is available 
        pass
    
    def link_ui(self, downloader, manager, data, link_failure=False):
        super().link_ui(downloader, manager, data, link_failure)
        for dw in self.device_widgets:
            dw.link_ui(downloader)
        
    def setup_ui(self, manager, data):
                        
        layout = get_layout(manager, data.layout_name)
        
        uic.loadUi(find_ui(layout.ui_file), self)                        
        self.device_widgets = layout.device_widget_list(manager, self)
        
        if layout.size:
            self.setMinimumSize(*layout.size)
                
        super().setup_ui(manager, data)
            
        for dw in self.device_widgets:
            dw.setup_ui()   
    
    def unlink_ui(self):
        super().unlink_ui()
        for dw in self.device_widgets:
            dw.unlink_ui()           


class ManagerUi(QWidget, BaseUi):
    def new_data(self,**kwargs):
        return ManagerData(**kwargs)
    
    def init_ui(self):    
        
        l = QGridLayout()
        self.setLayout(l)  
        
        self.name = QLabel()
        self.device_frame = ManagerDevices()
        self.ctrl_widget = ManagerCtrl()
        
        l.addWidget(self.name)
        l.addWidget(self.ctrl_widget)
        l.addWidget(self.device_frame)
                
        self.resize(750, 1000)
        
        
    
    def link_ui(self, downloader, manager, data, link_failure=False):
        super().link_ui(downloader, manager, data, link_failure)
        self.ctrl_widget.link_ui(downloader, manager, data)
        self.device_frame.link_ui(downloader, manager, data)
        
    def unlink_ui(self):
        self.ctrl_widget.unlink_ui()
        self.device_frame.unlink_ui()
    
    def change_layout(self, downloader, manager, data, layout):
        data.layout_name = layout
        self.device_frame.unlink_ui()
        self.device_frame.setParent(None)
        
        self.device_frame = ManagerDevices()        
        self.device_frame.setup_ui(manager, data)
        self.device_frame.link_ui(downloader, manager, data)        
        self.layout().addWidget(self.device_frame)
        
    def setup_ui(self, manager, data):        
        super().setup_ui(manager, data)
        
        self.ctrl_widget.setup_ui(manager, data)
        self.device_frame.setup_ui(manager, data)
                
        if hasattr(self, "name"):
            self.name.setText(data.name or manager.key)    

def _layout_switcher(w, downloader, manager, data, layout):
    def change_layout():
        w.main.change_layout(downloader, manager, data, layout)
    return change_layout

class ManagerMain(QMainWindow, BaseUi):
    views=None
    def init_ui(self):
        self.main = ManagerUi()
        self.setCentralWidget(self.main)
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
        
        
    def new_data(self, **kwargs):
        return ManagerData(**kwargs)
        
    def unlink_ui(self):
        self.main.unlink_ui()
        if self.views:
            for layout, viewAct in self.views.items():
                viewAct.triggered.disconnect()
    
    def link_ui(self, downloader, manager, data, link_failure=False):
        super().link_ui(downloader, manager, data, link_failure)
        self.main.link_ui(downloader, manager, data)
        if self.views:
            for layout, viewAct in self.views.items():
                # def change_layout(__layout__=layout):
                #     layout = __layout__ # make a local copy
                #     self.main.change_layout(downloader, manager, data, layout)
                # #f = lambda __l__=layout: self.main.change_layout(downloader, manager, data, __l__)
                # viewAct.triggered.connect(change_layout)
                viewAct.triggered.connect(_layout_switcher(self,downloader, manager, data, layout))
                 
    def setup_ui(self, manager, data):
        super().setup_ui(manager, data)        
        self.main.setup_ui(manager, data) 
        
        self.views = {}
        for layout in device_layouts(manager):
            viewAct = QAction(layout, self)
            self.viewMenu.addAction(viewAct)
            self.views[layout] = viewAct
        
        
        
        