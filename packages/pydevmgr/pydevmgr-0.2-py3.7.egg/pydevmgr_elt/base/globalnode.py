from pydevmgr_core import BaseNode, ksplit, kjoin
from typing import Callable, Optional, Any, Dict

class GlobalNode(BaseNode):
    """ This is a node attached to a device ot manager 
    
    This shall fill up a global_data dictionary. 
    This is used to store the python session data (for guis, etc... and not on OPC-UA) 
    """
    def __init__(self,  
          key: str, 
          global_data: Dict, 
          default: Optional[Any] = None,
          parser: Optional[Callable] = None
        ) -> None:
        super().__init__(key, parser=parser)
        
        self._global_data = global_data           
        self._default = default
        
    @classmethod
    def new(cls, 
          parent: Any, 
          name: str, 
          default: Optional[Any] = None,
          parser: Optional[Callable] = None, 
          
        ) -> BaseNode:
        """ Build a new :class:`GlobalNode` 
        
        The parent node shall have:
            - key attribute
            - global_data attribute
        
        Args:
            parent (any): mostlikely a :class:`UaInterface`
            name (str):  Node name 
            default (optional, Any): Default value if not in parent global_data
            parser (optional, callable): A value parser for the set method
        """
        return cls( kjoin(parent.key, name), parent.global_data, default=default, parser=parser )
    
    def fget(self) -> Any:
        """ get the value from server """
        return self._global_data.get( self.key, self._default )
    
    def fset(self, value: Any) -> None:
        """ set the value on server """        
        self._global_data[self.key] = value
        