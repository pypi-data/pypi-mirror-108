from pydevmgr.base.uadevice import DeviceConfig, UaCom, UaDevice
from pydevmgr.base.uamanager import ManagerConfig
 
from pprint import pprint  
host_mapping = {'opc.tcp://192.168.1.13:4840':'http://google.com'}
import yaml

cm = """
server_id           : 'ins1.fcs1'

ins1.fcs1:
    req_endpoint    : "zpb.rr://127.0.0.1:12082/"
    pub_endpoint    : "zpb.ps://127.0.0.1:12345/"
    db_endpoint     : "127.0.0.1:6379"
    db_timeout      : 2
    scxml           : "tins/sm.xml"
    dictionaries    : ['dit/stddid/primary.did', 'tins/fcf.did']
    fits_prefix     : "FCS1"
    #devices         : ['shutter1', 'lamp1', 'motor1', 'adc1', 'drot1', 'sensor1', 'ccc1', 'piezo1', 'actuator1']
    devices         : ['shutter1', 'lamp1',  'motor1', 'motor2', 'adc1', 'drot1']
    #devices         : ['motor1', 'motor2']
    cmdtout         : 60000

shutter1:
  type: Shutter
  cfgfile: "tins/shutter1.yml"

lamp1:
  type: Lamp
  cfgfile: "tins/lamp1.yml"

motor1:
  type: Motor
  cfgfile: "tins/motor1.yml"

motor2:
  type: Motor
  cfgfile: "tins/motor2.yml"
  
sensor1:
  type: Sensor
  cfgfile: "tins/sensor1.yml"

ccc1:
  type: Sensor
  cfgfile: "tins/ccc1.yml"

drot1:
  type: Drot
  cfgfile: "tins/drot1.yml"

adc1:
  type: Adc
  cfgfile: "tins/adc1.yml"
"""
c = """
type: Motor
interface: Softing
identifier: PLC1
prefix: MAIN.Motor1
simulated: false
ignored: false
address: opc.tcp://192.168.1.13:4840
simaddr: opc.tcp://127.0.0.1:7578
#mapfile: "tins/mapMotor.yml"
mapfile: ''
fits_prefix: "MOT1"
ctrl_config: {}
velocity:              3.0
min_pos:               0.0
max_pos:               359.0
axis_type:             CIRCULAR
active_low_lstop:      false
active_low_lhw:        false
active_low_ref:        true
active_low_index:      false
active_low_uhw:        true
active_low_ustop:      false
brake:                 false
low_brake:             false
low_inpos:             false
backlash:              0.0
tout_init:             30000
tout_move:             120000
tout_switch:           10000
initialisation:
  sequence: ['FIND_LHW', 'FIND_UHW', 'CALIB_ABS', 'END']
  FIND_LHW:
     value1: 4.0
     value2: 4.0
  FIND_UHW:
     value1: 4.0
     value2: 4.0
  CALIB_ABS:
     value1: 0.0
     value2: 0.0
  END:
     value1: 0.0
     value2: 0.0
positions:
    posnames: ['ON', 'OFF']
    tolerance: 1                              # Tolerance in UU
    "ON": 30
    "OFF": 100
"""

from pydantic import AnyUrl  

#cfg_dict = io.load_config('tins/motor1.yml')['motor1']
cfg_dict = yaml.load(c, Loader=yaml.CLoader)
#del cfg_dict['ctrl_config']
#cfg_dict['address'] = ""
cfg = DeviceConfig(**cfg_dict)  
#cf.ctrl_config['qqqq'] = 999
pprint(cfg.dict())

print("==============")

cfg = DeviceConfig(type="Shutter", uacom=UaCom('opc.tcp://192.168.1.13:4840'), prefix='MAIN.Shutter1')
pprint(cfg.dict())


dev = UaDevice('shutter', config=cfg)
print("==============")

cfg_dict = yaml.load(cm, Loader=yaml.CLoader)
#del cfg_dict['ctrl_config']
#cfg_dict['address'] = ""
cfg = ManagerConfig(**cfg_dict)  
pprint(cfg.dict())

# 
# 
# class INITSEQ:
#     END = 0
#     FIND_INDEX = 1
#     FIND_REF_LE = 2
#     FIND_REF_UE = 3
#     FIND_LHW = 4
#     FIND_UHW = 5
# 
#     DELAY = 6
#     MOVE_ABS = 7
#     MOVE_REL = 8
#     CALIB_ABS = 9
#     CALIB_REL = 10
#     CALIB_SWITCH = 11
# 
# class SeqStepCfg(CfgModel):
#     index : int = 0    
#     value1: float = 0.0
#     value2: float = 0.0
# 
# class InitialisationConfig(CfgModel):
#     sequence : List[str] = []
#     END          : SeqStepCfg = SeqStepCfg(index=1) 
#     FIND_INDEX   : SeqStepCfg = SeqStepCfg(index=2)
#     FIND_REF_LE  : SeqStepCfg = SeqStepCfg(index=3)
#     FIND_REF_UE  : SeqStepCfg = SeqStepCfg(index=4)
#     FIND_LHW     : SeqStepCfg = SeqStepCfg(index=5)
#     FIND_UHW     : SeqStepCfg = SeqStepCfg(index=6)  
#     DELAY        : SeqStepCfg = SeqStepCfg(index=7)
#     MOVE_ABS     : SeqStepCfg = SeqStepCfg(index=8)
#     MOVE_REL     : SeqStepCfg = SeqStepCfg(index=9)
#     CALIB_ABS    : SeqStepCfg = SeqStepCfg(index=10)
#     CALIB_REL    : SeqStepCfg = SeqStepCfg(index=11)
#     CALIB_SWITCH : SeqStepCfg = SeqStepCfg(index=12)
#     Indexes = INITSEQ    
#     @validator('END', 'FIND_INDEX', 'FIND_REF_LE', 'FIND_REF_UE', 'FIND_LHW', 'FIND_UHW', 
#                'DELAY', 'MOVE_ABS', 'MOVE_REL', 'CALIB_ABS', 'CALIB_REL' , 'CALIB_SWITCH'  )
#     def force_index(cls, v, field):
#         v.index = getattr(INITSEQ, field.name)
#         return v
# 
#     @validator('sequence')
#     def validate_initialisation(cls,sequence):   
# 
#         for s in sequence:
#             try:
#                 cls.__fields__[s]
#             except KeyError:
#                 raise ValueError(f'unknown sequence step {s!r}')
#         return sequence
# 
# class MotorConfig(DeviceConfig):
#     initialisation : InitialisationConfig = InitialisationConfig()
#     positions: Dict = {}    
# 
