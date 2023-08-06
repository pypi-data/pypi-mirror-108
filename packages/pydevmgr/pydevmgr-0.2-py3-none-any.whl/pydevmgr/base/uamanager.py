from pydevmgr_core import (NodeAlias, BaseNode, kjoin, ksplit, BaseInterface, InterfaceProperty, 
                           BaseManager, AllTrue, upload)

from . import io
from .uadevice import UaDevice, DeviceConfig, DeviceIOConfig, Recorder, DeviceIterator
from .tools import fsplit, fjoin
import logging
from collections import OrderedDict
from warnings import warn

from pydantic import BaseModel, root_validator, validator, AnyUrl
from typing import List, Type, Optional, Dict, Union, Iterable

class ServerConfig(BaseModel):
    """ Configuration Model of a server configuration as writen in a manager yml file """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    fits_prefix: str = ""
    devices : List[str] = [] # list of device names 
    cmdtout : int = 60000    # not yet used in pydevmgr 
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Config of BaseModel see pydantic 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:
        extra = "ignore"
                        
class ManagerConfig(BaseModel):
    """ Manager Configuration Model """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name: str = "" # if None takes the server_id 
    server  : ServerConfig = None
    devices : Dict[str,DeviceIOConfig] = None
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Config of BaseModel see pydantic 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config:
        extra = "ignore"   
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      
    @root_validator(pre=True)
    def init_values(cls, values):
        """ allowing the initialisation from .yml files as defined by eso """
        sid = values.get('server_id', None)
        
        
        if sid and not values.get('name', None):
            values['name'] = sid
        
        if values.get('server', None) is None:
            
            if not sid: # build an empty  ServerConfig and return 
                values['server'] = ServerConfig()
                if values.get('devices', None) is None:
                    values['devices'] = {}
                return values
            
            try:
                server = values.pop(sid)
            except KeyError:
                raise ValueError(f'{sid!r} dictionary is missing')
            # build ServerConfig from what is defined on the file     
            values['server'] = ServerConfig(**server)
            device_names = server.get('devices', [])
            
            # Then build the devices dictionary 
            devices = OrderedDict()            
            for name in device_names:
                try:
                    devio = values.pop(name)
                except KeyError:
                    raise ValueError(f'{name!r} is missing')
                devices[name] = DeviceIOConfig(name=name, **devio)
            values['devices'] = devices

        return values
    
    
    
class ManagerIOConfig(BaseModel):
    """ Config Model holding the I/O of a manager configuration """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name      : str = ""
    cfgfile   : Optional[str] = None
    config    : ManagerConfig = None # built from cfgfile if None
    extrafile : Optional[str] = None # extra is a pydevmgr thing. Used to defined guis layout for instance
    extra     : Dict = None # extracted from extrafile 
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    @validator('config', always=True, pre=True)
    def load_config(cls, config, values):
        if config is None:
            cfgfile = values['cfgfile']
            if cfgfile:
                return ManagerConfig(name=values['name'], **io.load_config(cfgfile))
            else:
                return ManagerConfig(name=values['name'])
        return config
    
    @validator('extra', always=True, pre=True)
    def load_extra(cls, extra, values):
        if extra is None:
            extrafile = values['extrafile']
            if extrafile:
                return io.load_config(extrafile)
            else:
                cfgfile = values['cfgfile']
                if cfgfile:
                    return io.load_extra_of(cfgfile) or {}
                return {}
        return extra
    

def load_manager_config(file_name: str, extrafile: Optional[str] =None) -> ManagerIOConfig:
    """ load a manager configuration from its yml file 
    
    Args:
        file_name (str): relative path to a configuration file 
                  The path is relative to one of the directory defined in the
                  $RESPATH environmnet variable or it can be an absolute path  
    """
    return ManagerIOConfig(cfgfile=file_name, extrafile=extrafile)



## #######################################################
#
#   Some NodeAlias for the manager 
#   These are created in the .stat UaInterface property
#

class SubstateNodeAlias(NodeAlias):
    """ Attempt to build one substate out of severals """
    SUBSTATE = UaDevice.SUBSTATE
    
    def fget(self, *substates) -> int:        
        if not substates: return self.SUBSTATE.UNKNOWN
        first = substates[0]
        if all( s==first for s in substates):
            return first 
        return self.SUBSTATE.UNKNOWN

class DevicesState(NodeAlias):
    """ Node Alias that define one state out of several devices node states """
    STATE = UaDevice.STATE
    
    @classmethod
    def new(cls, parent, name):
        """ requirement for the parent is to have: 
        
        - the devices() method  (e.g. ManagerStatInterface or Manager)
        """
        l = [d.stat.state for d in parent.devices() ] + [d.ignored for d in parent.devices() ]        
        return cls(parent.join_key(name), l)
    
    def fget(self, *states_ignore) -> int:
        """ return STATE.OP if all devices are in STATE.OP, STATE.NOTOP otherwhise """
        N = len(states_ignore)
        states = states_ignore[:N//2]
        ignored = states_ignore[N//2:]
        states = [s for s,i in zip(states, ignored) if not i]
        
        if all( s==self.STATE.OP for s in states ):
            return self.STATE.OP
        return self.STATE.NOTOP
        
class InitialisedNodeAlias(NodeAlias):    
    def fget(self, *init_flags):
        return all(f for f in init_flags)

##
# The stat manager for stat interface will be build of NodeAliases only 
#  
class ManagerStatInterface(BaseInterface):
    """ Special definition of Stat Interface for a Manager """
    STATE = UaDevice.STATE
    def __init__(self, key, devices):
        super().__init__(key)
        self._devices = devices        

    def devices(self) -> Iterable:
        return self._devices
        
    @classmethod
    def new(cls, parent, name):
        """ build a :class:`ManagerStatInterface` from its parent context 
        
        parent is mostlikely a :class:`UaManager`
        
        requirement for the parent is to have: 
        
        - the devices() method
        """        
        return cls( parent.key , parent.devices())        
    
    state = DevicesState.prop('state')    
        
    @NodeAlias.prop("state_txt", ["state"])
    def state_txt(self, state: int) -> str:
        """ text representation of the state """
        return self.STATE(state).txt
    
    @NodeAlias.prop("state_group", ["state"])
    def state_group(self, state: int) -> state:
        """ group of the state """
        return self.STATE(state).group
            
class UaManager(BaseManager):
    """ UaManager object, handling several devices 
    
    .. note::
    
        Most likely the UaManager will be initialized by :meth:`UaManager.from_config` or its alias :func:`open_manager`
    
    If :meth:`UaManager.from_config` or :func:`open_manager` is used all the device prefixes will be
    the key of the device manager.  
    
    Args:
        key (str): the key (prefix of all devices) of the manager
                If None key is the 'server_id' defined inside the config dictionary
        devices (dict, :class:`ManagerConfig`, class:`ManagerIOConfig`): 
                  if dictionary it is 
                        name/:class:`UaDevice` pairs 
                    or  name/:class:`DeviceConfig` pairs 
                    or  name/:class:`DeviceIOConfig` pairs 
                
        fits_key (str, optional): the Fits keyword (if ever used) of the manager. 
        cmdtout (int, optional): default timeout (not used yet)
        extra (dict, Optional): extra configuration for GUI layout definition. a pydevmgr feature (not ESO)            
                If None can be extracted from  ``devices`` if it is a class:`ManagerIOConfig`      
    
    """
    
    Device = UaDevice # default device class
    Config = ManagerConfig
    
    StatInterface = ManagerStatInterface    
    stat = InterfaceProperty('stat', cls='StatInterface')
    global_data = None
    
    dev_type = "Manager"
    
    def __init__(self, 
          key : str, 
          devices : Union[ManagerConfig,ManagerIOConfig,Dict[str,DeviceIOConfig], Dict[str, DeviceConfig], Dict[str, UaDevice]], 
          fits_key: str ='', 
          cmdtout: int =60000, 
          extra : Optional[Dict] =None,
          global_data: Optional[Dict] = None
        ) -> None:
        
        if isinstance(devices, ManagerConfig):
            config = devices
            devices = config.devices
            
        elif isinstance(devices, ManagerIOConfig):
            ioconfig = devices
            if extra is None:
                extra = ioconfig.extra
            
            config =  ioconfig.config
            devices = config.devices    
        
        global_data = {} if global_data is None else global_data
                    
        self._devices = OrderedDict()                
        for name, device in devices.items():
            if isinstance( device, DeviceIOConfig):
                self._devices[name] = Recorder.get_device_type(device.type, UaDevice)(kjoin(key, name), device.config, global_data=global_data)
            elif isinstance( device, DeviceConfig):
                self._devices[name] = Recorder.get_device_type(device.type, UaDevice)(kjoin(key, name), device, global_data=global_data)
            else: # assuming this is a UaDevice
                self._devices[name] = device
        
        self._key = key 
        self._fits_key = fits_key
        self._extra = {} if extra is None else extra
        self._global_data = global_data
        
    def __getattr__(self,attr):
        """ whatever is defined in __dict__ if failed try for a device name """
        try:
            return self.__dict__[attr]
        except KeyError:
            try:
                return self.get_device(attr)
            except ValueError:
                raise AttributeError("%r"%attr)
    
    def __dir__(self):
        lst = [d.name for d in self.devices()]
        for sub in self.__class__.__mro__:
            for k in sub.__dict__:
                if not k.startswith('_'):
                    lst.append(k)
        return lst 
    
    @property
    def key(self) -> str:
        return self._key
    
    # @property
    # def prefix(self):
    #     return ksplit(self._key)[0]
    
    @property
    def name(self) -> str:
        return ksplit(self._key)[1]
        
    @property
    def fits_key(self) -> str:
        return self._fits_key
    
    @property
    def fits_name(self) -> str:
        return fsplit(self._fits_key)[1]

    @property
    def fits_prefix(self) -> str:
        return fsplit(self._fits_key)[0]
    
    @property
    def extra(self) -> dict:
        return self._extra
    
    
    @classmethod
    def from_config(cl, 
          file_name: str, 
          key: Optional[str] = None, 
          extra_file: Optional[str] = None, 
          fits_prefix: str = ''
        ) -> BaseManager:
        """ Create a :class:`UaManager` object from its yaml configuration file 
        
        Args:
            file_name (str): This is the relative path trought the yml file defining the manager. 
                    The file shall be present inside one of the directories defined by the 
                    $RESPATH environmnet variable.
            key (str, optional):  The key of the manager (which will be the prefix of all devices)
                   If not given key will be the 'server_id' keyword has defined in the configuration file
            extra_file (str): This is the path to an extra yml file where some specific pydevmgr configuration 
                   are writen. If not given an eventual FILE_NAME_extra.yml file will be load. 
                   FILE_NAME_extra.yml must be on the same directory than FILE_NAME.yml
                   So far in the _extra file is defined GUI configurations.
        """
        config = load_manager_config(file_name)
        
        key = config.config.name if key is None else key
        
        fits_key = fjoin(fits_prefix, config.config.server.fits_prefix) 
        return cl(key, config.config.devices, fits_key=fits_key, extra=config.extra)
        
    def connect(self) -> None:
        """ Connect all the opc-ua client of the devices """
        for device in self._devices.values():
            device.connect()
    
    def disconnect(self) -> None:
        """ disconnect all the opc-ua client of the devices """
        for device in self._devices.values():
            device.disconnect()
            
    def get_device(self, name: str) -> UaDevice:
        """ get device matching the name Raise ValueError if not found 
        Args:
           name (str): device name 
        """
        try:
            return self._devices[name]
        except KeyError:
            raise ValueError('Unknown device %r'%name)
    
    @property
    def devices(self) -> Iterable:
        """ an Iterable object of children :class:`UaDevice` like object """
        return DeviceIterator(self._devices)
        #return list(self._devices.values())

    def device_names(self) -> list:
        """ return a list of child device names """
        return list(self._devices.keys())
    
        
    ## These RPC should be on all devices
    def init(self) -> NodeAlias:
        """ Init all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_initialised: a :class:`NodeAlias` which result in True when all devices are initialised
                             can be used in the :func:`pydevmgr.wait` function 
            
        Exemple:
           
           ::
           
               wait( mgr.init() )
        """
        nodes = [device.init() for device in self.devices() if not device.ignored.get()]
        return AllTrue('init_all_finished', nodes)
        
    def enable(self) -> NodeAlias:
        """ Enable all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_enabled: a :class:`NodeAlias` which result in True when all devices are enabled
                             can be used in the :func:`pydevmgr.wait` function 
            
        Exemple:
           
           ::
           
               wait( mgr.enable() )        
        
        """
        nodes = [device.enable() for device in self.devices() if not device.ignored.get()]
        return AllTrue('enable_all_finished', nodes)
        
    def disable(self) -> NodeAlias:
        """ Disable all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_disabled: a :class:`NodeAlias` which result in True when all devices are disabled 
                             can be used in the :func:`pydevmgr.wait` function 
            
        Exemple:
           
           ::
           
               wait( mgr.disable_all() )   
        """
        nodes = [device.disable() for device in self.devices() if not device.ignored.get()]
        return AllTrue('disable_all_finished', nodes)        

    def reset(self) -> NodeAlias:
        """ Reset all child devices 
        
        devices with a ignored flag will be ignored 
        
        Returns:
            all_reseted: a :class:`NodeAlias` which result in True when all devices are reseted
                             can be used in the :func:`pydevmgr.wait` function 
            
        Exemple:
           
           ::
           
               wait( mgr.reset() )   
        
        """
        nodes = [device.reset() for device in self.devices() if not device.ignored.get()]
        return AllTrue('reset_all_finished', nodes)        
    
    def configure(self) -> None:
        """ Configure all devices 
        
        devices with a ignored flag will be ignored 
        """
        conf = {}
        for device in self.devices():
            if not device.ignored.get():
                conf.update( device.get_configuration() )
        upload(conf)
    
    
    def ignore_all(self):
        """ set ignored flag to True for  all devices """
        for device in self.devices():
            device.ignored.set(True)
    
    def unignore_all(self):
        """ set ignored flag to False for  all devices """
        for device in self.devices():
            device.ignored.set(False)
    
    ### deprecated 
    def connect_all(self) -> None:
        """ Deprecated use connect instead  """
        warn(DeprecationWarning("connect_all method will be removed use connect "))
        return self.connect()
    def disconnect_all(self) -> None:
        """ Deprecated use disconnect instead  """
        warn(DeprecationWarning("disconnect_all method will be removed use disconnect "))
        return self.disconnect()
    def init_all(self) -> NodeAlias:
        """ Deprecated use init instead  """
        warn(DeprecationWarning("init_all method will be removed use init "))
        return self.init()
    def enable_all(self) -> NodeAlias:
        """ Deprecated use enable instead  """
        warn(DeprecationWarning("enable_all method will be removed use enable "))
        return self.enable()
    def disable_all(self) -> NodeAlias:
        """ Deprecated use disable instead  """
        warn(DeprecationWarning("disable_all method will be removed use disable "))
        return self.disable()
    def reset_all(self) -> NodeAlias:
        """ Deprecated use reset instead  """
        warn(DeprecationWarning("reset_all method will be removed use reset "))
        return self.reset()
    def configure_all(self) -> None:
        """ Deprecated use configure instead  """
        warn(DeprecationWarning("configure_all method will be removed use configure "))
        return self.configure()    
    
def open_manager(
      file_name: str, 
      key: str ='', 
      extra_file: Optional[str] = None
    ) -> UaManager:
    """ Create a :class:`UaManager` object from its yaml configuration file 
    
    Args:
        file_name (str) : This is the relative path to the yml file defining the manager. 
                The file shall be present inside one of the directories defined by the 
                $RESPATH environmnet variable or it can be an absolute path.
        key (str, optional):  The key of the manager (which will be the prefix of all devices)
               If not given key will be the 'server_id' keyword has defined in the configuration file
        extra_file (str): This is the path to an extra yml file where some specific pydevmgr configuration 
               are writen. If not given a file FILE_NAME_extra.yml will be load if it exists. 
               FILE_NAME_extra.yml must be on the same directory than FILE_NAME.yml
               So far (v0.2) the _extra file is defined GUI layout configurations.
                 
    """
    return UaManager.from_config(file_name, key=key, extra_file=extra_file)





    