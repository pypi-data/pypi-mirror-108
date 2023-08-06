from pydevmgr.base.tools import EnumTool, enum_txt, enum_group
from enum import Enum 

class ERROR(EnumTool, int, Enum):    
    OK	                   = 0
    HW_NOT_OP              = 1
    LOCAL                  = 2
    
    UNREGISTERED = 999


enum_txt( {ERROR.OK:"This is OK"} )
enum_group( {ERROR.OK:"G1"})
assert ERROR.LOCAL==2
assert ERROR.LOCAL.txt == 'LOCAL'
assert ERROR.LOCAL is ERROR.LOCAL
ERROR.LOCAL.txt = 'LOCAL E'

#print(ERROR.LOCAL.__dict__)
assert ERROR.LOCAL.txt == 'LOCAL E'
assert ERROR(10).txt == 'UNREGISTERED'
assert ERROR(0).txt =="This is OK"
assert ERROR(0).group =="G1"

class A(EnumTool, int, Enum):
    X = 0
try:
    A(1)
except ValueError:
    pass
else:
    assert False

#print(list(ERROR))
   