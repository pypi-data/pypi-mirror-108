from pydevmgr_core.datamodel import  DataModel, NodeVar, DataLink, Field, StaticVar
from pydevmgr_core import LocalUtcNode, DequeNode, PosName, Downloader, node
from pydevmgr_elt import open_device, nodealias, wait
import time

motor = open_device('tins/motor1.yml', key="M")
            
@nodealias('test', motor.stat.pos_actual)
def pos_m(pos):
    return pos*1e-3            

motor.stat.posname = PosName('posname', motor.stat.pos_actual, {'on':2, 'off':3, 'toto':4}, 0.5, unknown="?")

posname = PosName.prop('posname', ['pos_actual'], poses={'on':2, 'off':3, 'toto':4}, tol=0.5, unknown="?")
static = node('two')(lambda: 2)


class Poses(DataModel):
    actual:  NodeVar[float] = Field(0.0, attr="pos_actual")
    target:  NodeVar[float] = Field(0.0, attr="pos_target") 
    name:     NodeVar[str]  = Field("",  node=posname)
    
class MotorStatData(DataModel):
    utc:         NodeVar[str]   = Field("", node=LocalUtcNode('utc'))
    pos_actual:  NodeVar[float] = 0.0  
    pos_target:  NodeVar[float] = 0.0        
    pos_target2: NodeVar[float] = Field(0.0, attr="pos_target")
    pos_m:       NodeVar[float] = Field(0.0, node=pos_m)
    posname:     NodeVar[str]   = Field("",  node=posname)
    
    poses: Poses = Field(Poses(), attr="")
    
class MotorData(DataModel):
    num  : int =1
    name : StaticVar[str] = ""
    stat : MotorStatData = MotorStatData()



d = MotorData()
l = DataLink(motor, d)

downloader = Downloader(l)
print( downloader._dict_nodes, downloader._dict_datalinks,  )
try:
    motor.connect()
    downloader.download()
    print(d)
    
    wait( motor.move_abs(0, 100) )
    motor.move_rel(10, 1.5)        
    for i in range(100):
        
        downloader.download()
        
        print( f'{d.name} {d.stat.poses.actual:.2f} {d.stat.poses.name}')
        time.sleep(0.01)
        
    
    
        
finally:
    motor.disconnect()

