from pydevmgr_core import  upload, NodeAlias, kjoin, ksplit, BaseDevice, NodeVar
from . import io
from .uainterface import UaInterface 
from .uarpcinterface import UaRpcInterface
from .uanode import UaNode
from .globalnode import GlobalNode
from .uacom import UaCom
from .tools import (fjoin, fsplit, enum_group, enum_txt, EnumTool)
from .config import mconfig, GROUP 

from enum import Enum

from typing import Dict, Optional, Type, List, Iterable, Union, Any
from pydantic import BaseModel,  AnyUrl,  validator, Field
import logging


class CtrlConfig(BaseModel):
    # nothing by default to declare here 
    class Config: # BaseModel configuration of pydantic 
        # ignore/allow extra stuff for auto setup
        extra = 'allow' 

class MapConfig(BaseModel):
    class Config:
        extra = 'allow'
    cfg : Dict[str,str]  = {}
    stat : Dict[str,str] = {}
    rpc : Dict[str, str] = {}    
    
class DeviceConfig(BaseModel):
    """ Base Config Model for Devices this can be extended for each devices """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    type: str = "Device"
    # AnyUrl  will valid the address to an url 
    # the url is first replaced on-the-fly if defined in host_mapping 
    address     : AnyUrl         = ""  
    prefix      : str            = ""
    fits_prefix : str            = ""    
    mapfile     : Optional[str]  = None # hautorize None mapfile to load a default when map is validated
    map         : Dict           = None # map loaded from mapfile if None 
    ignored     : bool           = False    
    namespace   : int            = Field(default_factory=lambda : mconfig.namespace)
    ctrl_config : CtrlConfig     = CtrlConfig()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Config of BaseModel see pydantic 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    class Config: # BaseModel configuration of pydantic 
        # ignore/allow extra stuff that if not used by pydevmgr 
        #  'allow' to include the extras in the model this is needed for multi-axis
        extra = 'allow' 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~         
    @validator('address', pre=True)
    def map_host(cls, url, values):
        """ replace the address on-the-fly if any defined in host_mapping dictionary """
        return mconfig.host_mapping.get(url, url) 
        
    @validator('mapfile')
    def validate_mapfile(cls, file):
        """ if mapfile given check if exists """
        if file:
            io.find_config(file)            
            return file
        return None
    
    @validator('map',  always=True, pre=True)
    def load_map(cls, map, values):
        """ validate the map dictionary: 
            - if None and mapfile given : load the map file 
            - if None and no mapfile : load a default one from device type
            - if no device type is given raise an ValueError 
        """        
        if map is None:
            try:
                mapfile = values['mapfile']
                dtype = values['type']
            except KeyError:
                raise ValueError('wrong mapfile or no type')
                
            if mapfile is None:
                map_d = io.load_default_map(dtype)
                map = next(iter(map_d.values()))      
            else:
                map_d = io.load_map(mapfile)
                try:
                    map = map_d[dtype]
                except KeyError:
                    raise ValueError("The associated map file does not contain type %r"%dtype)
        return map
############## ##############  DeviceConfig ############### ############## 


class DeviceIOConfig(BaseModel):
    """ Config Model holding the I/O of a device configuration 
    
    This is used for instance in a manager configuration file
    """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    name : str = "" # device name 
    type : str = "" # device type 
    cfgfile : Optional[str] = None # config file path
    config : DeviceConfig = None
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Validator Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    @validator('config', always=True, pre=True)
    def load_device(cls, config, values):
        """ validate the config load it from cfgfile if given """
        if config is None:
            if values['cfgfile'] is not None:            
                return load_device_config(values['cfgfile'], type=values['type'], name=values['name'])                    
            else:
                return DeviceConfig()
        return config
############## ##############  DeviceIOConfig ############### ############## 

def load_device_config(
      file_name : str, 
      type: str = None, 
      name: str = None, 
      Config: Optional[Type[DeviceConfig]] = None
    ) ->  DeviceConfig:
    """ load a device configuration 
    
    Args:
        file_name (str): relative path to a configuration file 
                  The path is relative to one of the directory defined in the
                  $RESPATH environmnet variable
        type (str, optional): Type of the device, if not given look into the loaded file
        name (str, None): The device name in the config file. 
                        If None the first device in the loaded configuration file is taken 
    """
    
    allconfig = io.load_config(file_name)
    if name is None:
        # get the first key 
        name = next(iter(allconfig))
        config = allconfig[name]
    else:
        try:
            config = allconfig[name]
        except KeyError:
            raise ValueError(f"Device {name!r} does not exists on device definition file {file_name!r}")    

    if Config is None:    
        if type is None:
            try:
                type = config['type']
            except KeyError:
                raise ValueError('type is missing')
        try:
            Dev = Recorder.get_device_type(type)
        except (KeyError, ValueError):
            logging.warning(f'type {type!r} is unknown landing to a standard, empty device')                
            Dev = UaDevice
        Config = Dev.Config
    
    return Config(**config)    

########################
### STATE 
class STATE(EnumTool, int, Enum):
    """ constant holder for device STATEs """
    NONE = 0
    NOTOP = 1
    OP = 2
    
    UNREGISTERED = -9999 # place holder for unregistered STATE
    
enum_group({
STATE.NONE  : GROUP.UNKNOWN,
STATE.NOTOP :  GROUP.NOK,
STATE.OP    :  GROUP.OK,
})

########################
### SUBSTATE 
class SUBSTATE(EnumTool, int, Enum):
    """ constant holder for device SUBSTATEs """
    # SUBSTATE are specific to each device
    # :TODO: is their common SUBSTATE for each device ? NOTOP_NOTREADY =  100
    #  NOTOP_READY = 101  ?
    NONE = 0
    NOTOP_NOTREADY = 100 # not sure these number are the same accros devices
    NOTOP_READY    = 101
    NOTOP_ERROR    = 199
    
    OP_ERROR =299
    
    UNREGISTERED = -9999 # place holder for unregistered SUBSTATE
    
enum_group({
  SUBSTATE.NONE                   : GROUP.UNKNOWN,
  SUBSTATE.NOTOP_NOTREADY         : GROUP.NOK,
  SUBSTATE.NOTOP_READY            : GROUP.NOK,
  SUBSTATE.NOTOP_ERROR            : GROUP.ERROR, 
  SUBSTATE.OP_ERROR               : GROUP.ERROR, 
})

    
    
########################
### ERROR  
class ERROR(EnumTool, int, Enum):
    """ constant holder for device ERRORs """
    OK	                   = 0
    HW_NOT_OP              = 1
    LOCAL                  = 2
    
    UNREGISTERED = -9999 # place holder for unregistered ERROR
    # etc...
enum_txt({
    ERROR.OK:		 'OK',
    ERROR.HW_NOT_OP: 'ERROR: TwinCAT not OP or CouplerState not mapped.',
    ERROR.LOCAL:	 'ERROR: Control not allowed. Motor in Local mode.',
    ERROR.UNREGISTERED: 'Unregistered ERROR'
        # etc ...
})


class RpcInterface(UaRpcInterface):
    pass

class CfgInterface(UaInterface):
    # nothing to declare
    pass
    
class StatInterface(UaInterface):
    ERROR = ERROR # needed for error_txt alias 
    SUBSTATE = SUBSTATE # needed for substate_txt node alias
    STATE = STATE 
    
    def __init__(self, 
          key: str, 
          uacom: UaCom, 
          map: dict, 
          ua_prefix: str, 
          ua_namespace: Optional[int] = None,
          ERROR:    Optional[Type[ERROR]] = None, 
          SUBSTATE: Optional[Type[SUBSTATE]] = None, 
          STATE:    Optional[Type[STATE]] = None
        ):
        super().__init__(key, uacom, map, ua_prefix, ua_namespace=ua_namespace)
        
        # redefine dynamicaly the ERROR, SUBSTATE and STATE constants 
        if ERROR:
            self.ERROR = ERROR
        if SUBSTATE:
            self.SUBSTATE = SUBSTATE
        if STATE:
            self.STATE = STATE
    
    @classmethod
    def new(cls, 
          parent: Any, 
          name: str, 
          map: Optional[dict] = None, 
          namespace: Optional[int] = None, 
          ERROR: Optional[Type[ERROR]] = None, 
          SUBSTATE: Optional[Type[SUBSTATE]] = None, 
          STATE: Optional[Type[STATE]] = None
        ):
        """ Create a new stat interface in the context of its parent object 
                                
        The parent object is most likely a :class:`UaDevice` and should have:
           - key attribute (str)
           - map attibute (dict)
           - ua_namespace attribute 
           - _uacom attibute 
           - join_uakey() method  
        
        Args:
            parent (Any):  see above
            name (str): The stat interface name (usualy same name as parent device)
            namespace (optional,int): UA namespace if not given take the parent one
            ERROR, SUBSTATE, STATE: Enums for ERROR, SUBSTATE and STATE 
          
        """
        if map is None:
            map = parent.map.get(name, {})
        if namespace is None:
            namespace = parent.ua_namespace
        # The name is not added to the parent key here 
        return cls( parent.key, parent._uacom, map, parent.join_uakey(), ua_namespace=namespace, 
                    ERROR=ERROR, SUBSTATE=SUBSTATE, STATE=STATE )
    
    
    @NodeAlias.prop("is_operational", "state")
    def is_operational(self, state: int) -> bool:
        """ True if device is operational """
        return state == self.STATE.OP
    
    @NodeAlias.prop("is_not_operational", ["state"])
    def is_not_operational(self, state: int) -> bool:
        """ True if device not operational """
        return state == self.STATE.NOTOP
    
    @NodeAlias.prop("is_ready", ["substate"])
    def is_ready(self, substate: int) -> bool:
        """ True if device is ready """
        return substate == self.SUBSTATE.NOTOP_READY
    
    @NodeAlias.prop("is_not_ready", ["substate"])
    def is_not_ready(self, substate: int) -> bool:
        """ True if device is not ready """
        return substate == self.SUBSTATE.NOTOP_NOTREADY
    
    @NodeAlias.prop("is_in_error", ["substate"])
    def is_in_error(self, substate: int) -> bool:
        """ -> True is device is in error state:  NOP_ERROR or OP_ERROR """
        return substate in [self.SUBSTATE.NOTOP_ERROR, self.SUBSTATE.OP_ERROR]
    
    @NodeAlias.prop("substate_txt", ["substate"])
    def substate_txt(self, substate: int) -> str:
        """ Return a text representation of the substate """
        return self.SUBSTATE(substate).txt
    
    @NodeAlias.prop("substate_group", ["substate"])
    def substate_group(self, substate: int):
        """ Return the afiliated group of the substate """
        return self.SUBSTATE(substate).group

    
    @NodeAlias.prop("state_txt", ["state"])
    def state_txt(self, state: int) -> str:
        """ Return a text representation of the state """
        return self.STATE(state).txt

    @NodeAlias.prop("state_group", ["state"])
    def state_group(self, state: int):
        """ Return the afiliated group of the state """
        return self.STATE(state).group
    
    @NodeAlias.prop("error_txt", ["error_code"])
    def error_txt(self, error_code: int) -> str:
        """ Return the text representation of an error or '' if no error """
        return self.ERROR(error_code).txt
    
    @NodeAlias.prop("error_group", ["error_code"])
    def error_group(self, error_code: int) -> str:
        """ Return the text representation of an error or '' if no error """
        return GROUP.ERROR if error_code else GROUP.OK
        
class UaDevice(BaseDevice):
    """ Base class for OPC-UA ESO compliant Device object 
    
    Most likely a Device will be created by :func:`UaDevice.from_config` from a yml config file
    
    Args:
        key (str): device key (prefix of all nodes)
        config (optional, :class:`DeviceConfig`, :class:`DeviceIOConfig`, dict)
            Device class:`DeviceConfig` structure as returned by :func:`load_device_config` from a file 
            This can also be a dictionary which will be parsed into :class:`DeviceConfig`
            A :class:`DeviceIOConfig` is also accepted 
        uacom (optional, :class:`UaCom`): UaCom object setting the UA communication. If not given a new one is 
            created thanks to config.address attribute
        fits_prefix (str): prefix for fits keywords
        **kwargs :  **only used if config is a dictionary** kwargs overwrite any parameter in the config dictionary 
    """
    STATE = STATE
    SUBSTATE = SUBSTATE
    ERROR = ERROR
    
    _uacom = None
    _cfg = None 
    _global_data = None
    
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    
    ignored = GlobalNode.prop('ignored', default=False)
    
    Config = DeviceConfig
    
    _devices = None # some device can have child devices (e.g. ADC)
    _config_file = None
    def __init__(self,
          key: str, 
          config: Optional[Union[DeviceConfig,DeviceIOConfig,dict]] = None, 
          uacom: Optional[UaCom] = None, 
          fits_prefix: str ='', 
          global_data: Optional[Dict] = None, **kwargs
        ) -> None:
        
        if config is None:
            config = {}
        if isinstance(config, dict):
            config = {**config, **kwargs}
            
            if Recorder.has_device_type(self.__class__.__name__):
                # If the class was recorded with the good name, set the 
                # default type as the class name. It will allow to load of 
                # default mapping files  
                config.setdefault('type', self.__class__.__name__)
                
            config = self.Config.parse_obj(config)
        
        elif isinstance(config, DeviceIOConfig):
            self._config_file = config.cfgfile   
            config = config.config
             
        elif not isinstance(config, self.Config):
            raise ValueError('config must be a dictionary of a {} got a {}'.format(type(self.Config) , type(config)))
        
        self._config = config
        self._key =  key or ''
                
        # what is called prefix in config is actually a name here
        self._fits_key = fjoin(fits_prefix, self._config.fits_prefix)
        
        # init the client
        if uacom is None:
            self._uacom = UaCom(config.address)
        else:
            self._uacom = uacom
        
        self._global_data = {} if global_data is None else global_data
        
        self._devices = []
            
    def __repr__(self):
        return "<{} key='{}'>".format(self.__class__.__name__, self._key)
    
    @classmethod
    def from_config(cl, 
          file_name: str, 
          name: Optional[str] = None,
          key: Optional[str] = None, 
          fits_prefix : str =''
        ) -> BaseDevice:
        """ read a device configuration file and return a :class:`Device` like object to handle it 
        
        Args:
            file_name (str): relative path to a configuration file 
                      The path is relative to one of the directory defined in the
                      $RESPATH environmnet variable
            name (str,None): The device name in the config file. 
                      If None take the first device of the configuration file
                    
                For instance in config file like
                    
                    :: 
                         
                        motor1:
                          type: Motor
                          interface: Softing
                          identifier: PLC1
                          etc... 
                
                'motor1' is the `cfg_name`
            
            key (str, optional): The device key. If not given cfg_name is taken
            fits_prefix (str, optional): The fits prefix string for this device
        """
        
        config = load_device_config(file_name, name=name, Config=cl.Config)
        if key is None:
            key = name        
        return cl(key, config, fits_prefix=fits_prefix)
        
    @classmethod
    def load_config(cl, 
          file_name : str, 
          name : Optional[str] = None, 
          **kwargs
        )  -> DeviceConfig: 
        return load_device_config(file_name, type=None, name=None)
    
    @property
    def config(self) -> DeviceConfig:
        return self._config
    
    @property
    def global_data(self) -> Dict:
        return self._global_data
        
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
    def address(self) -> str:  
        return self.config.address      
    
    @property
    def ua_prefix(self) -> str:
        return self.config.prefix
        
    @property
    def ua_namespace(self) -> int:
        return self.config.namespace
        
    @property
    def dev_type(self) -> str:
        return self.config.type
    
    @property
    def map(self) -> dict:
        """ map dictionary """
        return self.config.map
    
    @property
    def devices(self) -> Iterable:
        """ an Iterable object of children :class:`UaDevice` like object 
        
        This make sens only for device containing sub-devices (e.g. ADC)
        """
        return DeviceIterator(self._devices)
        #return list(self._devices.values())
    
    def get_device(self, name: str) -> BaseDevice:
        """ get device matching the name Raise ValueError if not found
        
        This make sens only for device containing sub-devices (e.g. ADC) 
        
        Args:
           name (str): device name 
        """
        try:
            return self._devices[name]
        except KeyError:
            raise ValueError('Unknown device %r'%name)
    
    def join_uakey(self, *names) -> str:
        """ join keys together with the device prefix """        
        names = (self.ua_prefix,)+names
        return ".".join(a for a in names if a)
    
    def connect(self) -> None:
        """ Establish a client connection to OPC-UA server """
        self._uacom.connect()

    def disconnect(self) -> None:
        """ disconnect the OPC-UA client """
        self._uacom.disconnect()
            
    def is_connected(self) -> bool:
        """ Return True if the current device is connected to OPC-UA """
        return self._uacom.is_connected()        
                    
    def clear(self) -> None: 
        """ clear some cached values """ 
        for k,v in list(self.__dict__.items()):
            if isinstance(v, (UaInterface, UaRpcInterface)):
                v.clear()
                self.__dict__.pop(k)
    
    ## These RPC should be on all devices
    def init(self) -> UaNode:
        """ init the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code
        
        Returns: 
            is_ready:  the :class:`NodeAlias` .stat.is_ready to check if the init is finished 
        
        Exemple:
        
            ::
            
                wait( device.init() )
        
        """
        self.rpc.rpcInit.rcall()
        return self.stat.is_ready
        
    def reset(self) -> UaNode:
        """ reset the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code
        
        Returns:
           is_not_ready:  the :class:`NodeAlias` .stat.is_not_ready to check if the reset was done 
        
        ::
            
            wait( device.reset() )
        
        """
        self.rpc.rpcReset.rcall()
        return self.stat.is_not_ready

    def enable(self) -> UaNode:
        """ enable the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code
        
        Returns
             is_operational: the :class:`NodeAlias` .stat.is_operational to check if device was enabled 
        
        ::
            
            wait( device.enable() )
        
        """ 
        self.rpc.rpcEnable.rcall()
        return self.stat.is_operational
        
    def disable(self) -> UaNode:
        """ disable the device 
        
        Raises:
            RpcError:  if OPC-UA Rpc method  returns an error code 
             
        Returns: 
            is_not_operational:  the :class:`NodeAlias` .stat.is_not_operational to check if device was disabled 
        
        ::
            
            wait( device.disable() )
            
        """
        self.rpc.rpcDisable.rcall()
        return self.stat.is_not_operational
    
    
    def get_error_txt(self, errcode: int) -> str:
        """ Get a text description of the given error code number """
        return self.ERROR(errcode).txt
    
    def get_rpc_error_txt(self, rpc_errcode: int) -> str:
        """ Get a text description of the given rpc error code number """
        return self.RpcInterface.RPC_ERROR(rpc_errcode).txt
    
    def get_configuration(self, **kwargs):
        """ return a node/value pair dictionary ready to be uploaded 
        
        The node/value dictionary represent the device configuration. 
        This is directly use by :func:`Device.configure` method. 
        
        This is a generic configuration dictionary and may not work on all devices. 
        This method need to be updated for special devices for instance.   
        
        Args:
            **kwargs : name/value pairs pointing to cfg.name node
                      This allow to change configuration on the fly
                      without changing the config file.             
        
        ::
        
            >>> upload( {**motor1.get_configuration(), **motor2.get_configuration()) 
        """
        # get values from the ctrl_config Config Model
        # do not include the default values, if they were unset, the PLC will use the default ones
        values = self.config.ctrl_config.dict(exclude_none=True, exclude_unset=True)
        cfg_dict = {self.cfg.get_node(k):v for k,v in values.items()}
        cfg_dict[self.ignored] = self.config.ignored 
        cfg_dict.update({self.cfg.get_node(k):v for k,v in kwargs.items()})
        return cfg_dict
    
    def configure(self, **kwargs):
        """ Configure the whole device in the PLC according to what is defined in the config dictionary 
        
        Quick changes on configuration value can be done by keywords where each key must point to a 
        .cfg.name node. Note that the configuration (as written in file) is always used first before being 
        overwritten by **kwargs. In other word kwargs are not changing the default configuration  
        
        Args:
            **kwargs :  name/value pairs pointing to cfg.name node
                        This allow to quickly change configuration on the fly
                        without changing the config file.
                          
        
        what it does is just:
        
        ::
        
           >>> upload( self.get_condifuration() ) 
        """
        # by default just copy the "ctrl_config" into cfg. This may not work for
        # all devices and should be customized  
        upload(self.get_configuration(**kwargs))



# a loockup table for devices 
class Recorder:
    """ A global class acting as a lookup table to link string device type to a device Class constructor
    
    **This class is not intended to be instantiated** All methods are classmethods.
    """
    __device_types__ = {}
    @classmethod
    def new_device_type(cl, 
          type_name : str, 
          dev_cls : Type[UaDevice]
        ) -> None:
        """ record a new device to the UaManager class
        WARNING: the recorded or overwriten type will have effect on all new instance
                  of an UaManager
        """
        if not hasattr(dev_cls, 'from_config'):
            raise ValueError('class must have the `from_config` method')
        cl.__device_types__[type_name] = dev_cls
    
    @classmethod
    def get_device_type(cl, 
          type_name: str, 
          default: Optional[Type[UaDevice]] =None
        ) -> Type[UaDevice]:
        """ Return a :class:`UaDevice` type (constructor for device)"""
        try:
            return cl.__device_types__[type_name]
        except KeyError:
            if default is None:
                raise ValueError('Unknown device type %r '%type_name)
            else:
                return default    
    
    @classmethod
    def has_device_type(cl, type_name: str):
        return type_name in cl.__device_types__
        

Recorder.new_device_type('Device', UaDevice)    


class DeviceIterator:
    def __init__(self, devices):
        self._devices = devices
    
    def __iter__(self):
        return iter(self._devices.values())
    
    def __getitem__(self, item):
        return self._devices[item]
    
    def __call__(self):
        return list(self._devices.values())
    
    def names(self) -> Iterable:
        return list(self._devices)
    

def open_device(
      file_name: str, 
      cfg_name: Optional[str] = None, 
      key: Optional[str] = None, 
      prefix : str ='', 
      fits_prefix: str =''
    ) -> UaDevice:
    """ Read a device configuration file and return a :class:`UaDevice` like object to handle it 
    
    Args:
        file_name (str): relative path to a configuration file 
                  The path is relative to one of the directory defined in the
                  $RESPATH environmnet variable or it can be an absolute path 
        cfg_name (str, None): The device name in the config file. 
                  If None the first device in the configuration is taken 
                
            For instance in config file like
                
                :: 
                     
                    motor1:
                      type: Motor
                      interface: Softing
                      identifier: PLC1
                      etc... 
            
            'motor1' is the `cfg_name`
        
        key (str, optional): The device key. If not given prefix.cfg_name is taken
        prefix (str, optional): used only when key is None, key becomes `prefix`.`cfg_name` 
        fits_prefix (str, optional): The fits prefix string for this device
    """
    
    config = load_device_config(file_name, name=cfg_name)
    if key is None:        
        key = kjoin(prefix, cfg_name)
    
    cl = Recorder.get_device_type(config.type)        
    return cl( key, config, fits_prefix=fits_prefix)  



def open_devices(
      file_names: Iterable[str], 
      prefix : str =''
    ) -> List[UaDevice]:
    """ Open several devices in a list of (name, :class:`UaDevice`) tuple """
    devices = []
    for file_name in file_names:
        device = open_device(file_name, prefix=prefix)
        
        devices.append( (device.name, device) )
    return devices





#  ____    _  _____  _      __  __           _      _ 
# |  _ \  / \|_   _|/ \    |  \/  | ___   __| | ___| |
# | | | |/ _ \ | | / _ \   | |\/| |/ _ \ / _` |/ _ \ |
# | |_| / ___ \| |/ ___ \  | |  | | (_) | (_| |  __/ |
# |____/_/   \_\_/_/   \_\ |_|  |_|\___/ \__,_|\___|_|
# 

class BaseStatModel(BaseModel):
    """ Data Model class holding stat information of device """
    state : NodeVar[int] = 0
    substate: NodeVar[int] = 0
    error_code: NodeVar[int] = 0 
    
    ## Node Aliases 
    is_operational: NodeVar[bool] = False
    is_not_operational: NodeVar[bool] = False
    is_ready: NodeVar[bool] = False
    is_not_ready: NodeVar[bool] = False
    is_in_error: NodeVar[bool] = False
    
    substate_txt: NodeVar[str] = ""
    substate_group: NodeVar[str] = ""
    state_txt: NodeVar[str]  = ""
    state_group: NodeVar[str] = ""
    error_txt: NodeVar[str]  = ""    
    
