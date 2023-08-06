from .node import BaseReadCollector, BaseWriteCollector
from .rpc import BaseCallCollector

class BaseCom:   
    """ Define a BaseCom object 
    
    The Base does not do anything but is a place holder for what a com object should have
    A Com object can be set into a Device -> Interface -> Node for instance. 
    
    As for :class:`pydevmgr_core.BaseNode`: 
         - The sid property must return a unique id per server
         - get_collector must return an object to collect nodes for reading
         - set_collector must return an object to collect nodes for writing 
         - call_collector must return an object for Rpc call collection 
          
    """ 
    @property
    def sid(self):
        return 0 
    
    def connect(self):
        pass
    
    def disconnect(self):
        pass
    
    def read_collector(self):
        return BaseReadCollector()
    
    def write_collector(self):
        return BaseWriteCollector()
    
    def call_collector(self):
        return BaseCallCollector()