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
          vtype: Optional[Callable] = None
        ) -> None:
        super().__init__(key)
        
        self._global_data = global_data   
        self._vtype = vtype   
        self._default = default
        
    @classmethod
    def new(cls, 
          parent: Any, 
          name: str, 
          default: Optional[Any] = None,
          vtype: Optional[Callable] = None, 
          
        ) -> BaseNode:
        """ Build a new :class:`GlobalNode` 
        
        The parent node shall have:
            - key attribute
            - global_data attribute
        
        Args:
            parent (any): mostlikely a :class:`UaInterface`
            name (str):  Node name 
            default (optional, Any): Default value if not in parent global_data
            vtype (optional, callable): A value parser for the set method
        """
        return cls( kjoin(parent.key, name), parent.global_data, default=default, vtype=vtype )
    
    def fget(self) -> Any:
        """ get the value from server """
        return self._global_data.get( self.key, self._default )
    
    def fset(self, value: Any) -> None:
        """ set the value on server 
        
        Args:
            value (any): if :attr:`~UaNode.vtype` is defined it is used to parse the value
                can be str, float, int, or :class:`ua.Variant` or  :class:`ua.DataValue` 
        """
        if self._vtype:
            value = self._vtype(value)
        self._global_data[self.key] = value
        