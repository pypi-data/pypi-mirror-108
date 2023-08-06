from pydevmgr_core import DataLink
from pydevmgr_elt import open_device, wait
from pydevmgr.devices.motor import MotorStatModel, MotorCfgModel, MotorModel

try:
    m1 = open_device("tins/motor1.yml", "motor1") 
    m1.connect()
    m1.cfg.max_pos.set(359)
    ms = MotorStatModel()
    mc = MotorCfgModel()
    
    dls = DataLink(m1.stat, ms)
    dlc =  DataLink(m1.cfg, mc)
    
    dls.download()
    print(ms.pos_actual)
    
    wait( m1.move_abs(4, 40))
    dls.download()
    print(ms.pos_actual)
    
    dlc.download()
    print(mc.min_pos, mc.max_pos)
    
    m = MotorModel()
    dl = DataLink(m1 , m)
    dl.download()
    print( m.stat.pos_actual )
    
    
    
finally:
    m1.disconnect()
