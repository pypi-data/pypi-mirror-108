from pydantic import BaseModel
from .io import IOConfig


class GROUP:
    """ Constants holder GROUP are used to classify state and substates
    
    This class is not intended to be instancied but only to hold constants
    
    An application if for widget styling for instance : one style per group
    
        SUBSTATE.group[SUBSTATE.NOTOP_NOTREADY] == GROUP.NOK
    """
    # for substate 
    IDL      = "IDL"
    WARNING  = "WARNING"
    ERROR    = "ERROR"
    OK       = "OK"
    NOK      = "NOK"
    BUZY     = "BUZY"
    UNKNOWN  = "UNKNOWN"
    
    # for modes 
    STATIC = "STATIC",
    TRACKING = "TRACKING", 
    ENG = "ENG"
    
    



class MConfig(BaseModel):
    # default namespace 
    namespace: int = 4
    # this is a global mapping allowing to change the opc.tcp address on the fly 
    # usefull when switching from real PLC to simulated one without having to 
    # edit the config files. The key should be the full address to replce (including port)
    # e.g. host_mapping = {"opc.tcp://134.171.59.99:4840": "opc.tcp://192.168.1.13:4840"}
    host_mapping: dict = {}
    # input output configuration 
    io: IOConfig = IOConfig()

mconfig = MConfig()    
         