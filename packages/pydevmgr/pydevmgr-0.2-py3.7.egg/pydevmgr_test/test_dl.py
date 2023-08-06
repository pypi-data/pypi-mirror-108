from pydevmgr_elt import DataLink, open_manager, NodeVar
from pydantic import BaseModel, Field

class Data(BaseModel):
    
    pos1: NodeVar[float] = Field(0.0, attr="motor1.stat.pos_actual".split("."))
    pos2: NodeVar[float] = Field(0.0, attr="motor2.stat.pos_actual".split("."))



mgr = open_manager("tins/tins.yml")
data = Data()
dl = DataLink(mgr, data)

try:
    mgr.connect()
    dl.download()
    print('POS', data.pos1, data.pos2)
finally:
    mgr.disconnect()
    