from pydevmgr_core import NodeAlias, buildproperty, NodeVar, upload
from ..base.uadevice import (UaDevice, GROUP, Recorder)
from ..base.tools import  _inc, enum_group, enum_txt, EnumTool
from ..base.uacom import Int32, UInt32
from ..base.uanode import UaNode
from ..base.uarpc import UaRpc
from ..base.uainterface  import UaInterface
from ..base.uarpcinterface import UaRpcInterface


from pydantic import BaseModel
from enum import Enum

from typing import Optional

class CcsSimCtrlConfig(UaDevice.Config.CtrlConfig):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    latitude  : Optional[float] = -0.429833092 
    longitude : Optional[float] = 1.228800386

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
class CcsSimConfig(UaDevice.Config):
    CtrlConfig = CcsSimCtrlConfig
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data Structure 
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ctrl_config : CtrlConfig = CtrlConfig() 
    type: str = "CcsSim"
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 
##### ###########
# SUBSTATE
class TIME_MODE(EnumTool, int, Enum):
    LOCAL                  =   0    
    UTC                    =   1
    
    UNREGISTERED = -9999



#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class CcsSimStatInterface(UaInterface):
    TIME_MODE = TIME_MODE
    
    @NodeAlias.prop("time_mode_txt", ["time_mode"])
    def time_mode_txt(self, time_mode: int) -> str:
        """ Return a text representation of the time_mode """
        return self.TIME_MODE(time_mode).txt
    
    
@buildproperty(UaNode.prop, 'parser')      
class CcsSimCfgInterface(UaInterface):
    # we can define the type to parse value directly on the class by annotation
    latitude:    float
    longitude:  float

@buildproperty(UaNode.prop, 'parser')      
class CcsSimCtrlInterface(UaInterface):
    # we can define the type to parse value directly on the class by annotation
    temperature: float
    pressure: float
    humidity: float
    lapserate: float
    wavelength: float
    dut: float




@buildproperty(UaRpc.prop, 'args_parser') 
class CcsSimRpcInterface(UaRpcInterface):    
    rpcSetCoordinates : (float, float, float)


#  ____        _          __  __           _      _ 
# |  _ \  __ _| |_ __ _  |  \/  | ___   __| | ___| |
# | | | |/ _` | __/ _` | | |\/| |/ _ \ / _` |/ _ \ |
# | |_| | (_| | || (_| | | |  | | (_) | (_| |  __/ |
# |____/ \__,_|\__\__,_| |_|  |_|\___/ \__,_|\___|_|
# 

class CcsSimCfgData(BaseModel):
    latitude:  NodeVar[float] =  -0.429833092     
    longitude:  NodeVar[float] = 1.228800386    
  
class CcsSimCtrlData(BaseModel):
    temperature: NodeVar[float] = 0.0
    pressure: NodeVar[float] = 0.0
    humidity: NodeVar[float] = 0.0
    lapserate: NodeVar[float] = 0.0
    wavelength: NodeVar[float] = 0.0
    dut: NodeVar[float] = 0.0    
      
class CcsSimStatData(BaseModel):
    time_mode: NodeVar[int] = 0
    sdc_time: NodeVar[str]  = ""
    dc_time : NodeVar[int] = 0  
    
    apparent_alpha: NodeVar[float] = 0.0 
    apparent_delta: NodeVar[float] = 0.0 
    alpha :  NodeVar[float]  = 0.0 
    delta :  NodeVar[float]  = 0.0 
    ha :  NodeVar[float]  = 0.0  
    zd :  NodeVar[float]  = 0.0  
    az :  NodeVar[float]  = 0.0 
     
    
    temperature: NodeVar[float]  = 0.0  
    pressure: NodeVar[float]     = 0.0     
    humidity: NodeVar[float]     = 0.0     
    lapserate: NodeVar[float]    = 0.0    
    
    lst : NodeVar[float] = 0.0
    pa  : NodeVar[float] = 0.0
    pa_deg : NodeVar[float] = 0.0
    alt : NodeVar[float] = 0.0
    alt_deg : NodeVar[float] = 0.0
    ha: NodeVar[float] = 0.0
    az: NodeVar[float] = 0.0
    az_deg : NodeVar[float] = 0.0
    rotation: NodeVar[float] = 0.0
    rotation_deg : NodeVar[float] = 0.0
    ra: NodeVar[float] = 0.0
    dec: NodeVar[float] = 0.0
    
class CcsSimData(BaseModel):
    StatData = CcsSimStatData
    CfgData = CcsSimCfgData
        
    cfg: CfgData = CfgData()
    stat: StatData = StatData()    

#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#

class CcsSim(UaDevice):    
    
    Config = CcsSimConfig
    Data = CcsSimData
    
    StatInterface = CcsSimStatInterface
    CfgInterface = CcsSimCfgInterface
    RpcInterface = CcsSimRpcInterface
    
                
    stat = StatInterface.prop('stat')    
    cfg  = CfgInterface.prop('cfg')
    rpc  = RpcInterface.prop('rpc')
    
    def reset(self) -> UaNode:
        raise ValueError('CcsSim has no reset capability')

    def enable(self) -> UaNode:
        raise ValueError('CcsSim has no enable capability')
        
    def disable(self) -> UaNode:
        raise ValueError('CcsSim has no disable capability')
    
    def init(self) -> UaNode:
        raise ValueError('CcsSim has no init capability')
    
    def set_coordinates(self, ra: float, dec: float, equinox: float) -> None:
        self.rpc.rpcSetCoordinates.rcall(ra, dec, equinox)
    
    def set_environment(self, 
            temperature: Optional[float] = None, 
            pressure: Optional[float] =None, 
            humidity: Optional[float] =None, 
            lapserate: Optional[float] =None, 
            wavelength: Optional[float] = None, 
            dut: Optional[float] = None                              
        ):
        """ set environmnent data to the CCS Simulator 
        
        Each settings arguments are potional: 
          temperature, pressure, humidity, lapserate, wavelength, dut   
        
        """
        nodes = {}
        if temperature is not None:
            nodes[self.ctrl.temperature] = temperature
        
        if pressure is not None:
            nodes[self.ctrl.pressure] = pressure
        
        if humidity is not None:
            nodes[self.ctrl.humidity] = humidity
            
        if lapserate is not None:
            nodes[self.ctrl.lapserate] = lapserate    
        
        if wavelength is not None:
            nodes[self.ctrl.wavelength] = wavelength 
        
        if dut is not None:
            nodes[self.ctrl.dut] = dut        
        updload(nodes)          
        
Recorder.new_device_type('CcsSim', CcsSim)

