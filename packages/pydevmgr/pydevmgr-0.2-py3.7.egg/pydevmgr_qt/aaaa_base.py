from .io import find_ui, load_config

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLayout, QBoxLayout, QGridLayout, QWidget, QFrame


from pydantic import BaseModel, validator
from pydevmgr import NodeVar, DataLink, UaDevice, UaManager,  Downloader
from pydevmgr_core.download import DownloaderConnection
from typing import Optional, Dict , Union, Iterable, List
import glob 
from warnings import warn 
from dataclasses import dataclass
# TODO change the warning function to something else

class BaseUi:    
    _did_failed = False
    
    ## #############################################################
    #  
    #   Engine Methods
    #
    ## #############################################################
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()
    
    def _disconnect_me(self):
        # function to be overwrtiten by link_ui
        pass
    
    def link_ui(self, 
          downloader_or_connection: Union[Downloader,DownloaderConnection],
          device: UaDevice, 
          data :  BaseModel ,
          link_failure: Optional[bool] = False
          ) -> None:
        """ Link the UI to a downloader 
        
        Each time the downloader will "download" the update_ui will be executed with the 
        freshly updated data.
        
        Args:
            - downloader (:class:`pydevmgr.Downloader`)
            - device (:class:`pydevmgr.BaseDevice`)
            - data (:class:`BaseModel`)
            - link_failure (bool): if True, when download failed self.update_ui_failure will be executed
        """
        self._disconnect_me() # remove any connection 
               
        if isinstance(downloader_or_connection, Downloader):  
            connection  = downloader_or_connection.new_connection()
            new_connection = True 
        else:
            connection  = downloader_or_connection
            new_connection = False
        
        # The data is added to the queue of data to be downloaded 
        # y the downloader associated to the connection  
        dl =  DataLink(device, data)       
        connection.add_datalink(dl)
        
        def download_callback(dummy=None):
            self.update_ui(data)
        connection.add_callback(download_callback)
        
        if link_failure:
            connection.add_failure_callback(self.update_ui_failure)
        
        ##
        #  Overwrite the disconnect_me function 
        if new_connection:
            # we can simply disconnect the connection from the downloader all callback and datalink 
            # will be removed 
            def disconnect_me():
                connection.disconnect()
        else:       
            # the connection may be used somewhere else so remove only the created 
            # datalinks and callback 
            if link_failure:
                def disconnect_me():
                    connection.remove_datalink(dl)
                    connection.remove_callback(download_callback)
                    connection.remove_failure_callback(self.update_ui_failure)
            else:
                def disconnect_me():
                    connection.remove_datalink(dl)
                    connection.remove_callback(download_callback)
        self._disconnect_me = disconnect_me
        
    def link_and_setup_ui(self, 
           downloader: Downloader, 
           device: UaDevice, 
           link_failure: Optional[bool] = False, 
           **kwargs
         ) -> BaseModel:
         
        data = self.new_data(**kwargs)
        self.setup_ui(device, data)
        self.link_ui(downloader, device, data, link_failure=link_failure)        
        return data
        
    def unlink_ui(self) -> None:
        """ Free the ui from downloader connection callbacks 
        After executing unlink_ui, the refresh is stopped and widget actions are removed 
        """
        self._disconnect_me()        
        self.disconnect_events()
    
    def __del__(self):
        try:
            self.unlink_ui()
        except Exception as e:
            pass        

    ## #############################################################
    #
    #    Methods To be implemented 
    #
    ## #############################################################
    
    def disconnect_events(self):
        # disconnect all button or other action associiated to a device 
        # which has been connected by setup_ui              
        pass 
    
    def setup_ui(self, device: UaDevice, data: BaseModel) -> None:
        """ setup the UI for a input device and associated data 
        
        setup_ui change the static data and the actions associated to buttons, dropdown, etc ...
        """        
        # Disconnect all buttons, dropdoown, etc from previous connected events
        self.disconnect_events()
        # to be implemented 
        
    def update_ui_failure(self, er):
        self.setEnabled(False)        
        self._did_failed = True    
            
    def update_ui(self, data: BaseModel) -> None:
        """ update the ui to new data 
        
        Args:
           data (class:`pydantic.BaseModel`): Data Model as returned by .new_data() method            
        """
        pass    
    
    def init_ui(self) -> None:
        """ build the UI """
        raise NotImplementedError("init_ui")
    
    def new_data(self, **kwargs) -> BaseModel:
        """ Build and return a new data structure suitable for this UI 
        
        The datastructure is used by update_ui method 
        """        
        return BaseModel(**kwargs)
    


def device_widget(
      device: UaDevice, 
      widget_type: str ="ctrl", 
      check_status: Optional[Dict[str,bool]] = None):
    """ Create and return a QT widget for a given device 
    
    Args:
        - device (:class:`pydevmgr.UaDevice`): UA Device
        - widget_type (str): widget types. Builtin types are : 
            - 'ctrl' : a compact but complete control and state widget 
            - 'line' : one line very compact control and state widget 
        - check_status (optional, dict): 
            If given the dictionary will be filled up with device keys/check status pairs and 
            the .check box of the widget will be shown (if the widget has the .check checkbox)
            If None the checkbox of the widget (if exists) will be hidden 
    """
    try:
        Widget = get_widget_constructor(widget_type, device.dev_type)
    except ValueError:
        
        warn(Warning("Cannot find a %r widget for device of type %r"%(widget_type, device.dev_type)))
        Widget =   get_widget_constructor(widget_type, 'Device')
        
        widget = Widget()
        if check_status is not None:
            if hasattr(widget, "check"):
                widget.check.show()
                def checkChanged():
                    check_status[device.key] = widget.check.isChecked()
                widget.check.stateChanged.connect(checkChanged)
            



        
    
    