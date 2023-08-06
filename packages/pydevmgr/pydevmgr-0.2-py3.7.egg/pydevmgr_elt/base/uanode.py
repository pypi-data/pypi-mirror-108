from pydevmgr_core import BaseNode, ksplit, kjoin
from .uacom import UaComNode, UAReadCollector, UAWriteCollector
from .config import mconfig

import opcua
from opcua import ua
from typing import Callable, Optional, Any, Union
        
class UaNode(BaseNode):
    """ Object representing a value node in opc-ua server

    This is an interface representing one single value (node) in the OPC-UA server. 
    
    Node will be mostly used transparently inside :class:`Interface` object itself embeded inside 
    a :class:`pydevmgr.Device` object
    for instance  ```mgr.motor1.stat.pos_actual``
        
    where:
         
    - mgr: is a :class:`pydevmgr.Manager`
    - motor1: is a :class:`pydevmgr.Motor` extended from :class:`pydevmgr.UaDevice`
    - stat :  is a :class:`pydevmgr.UaInterface`  (group of nodes with a mapping dictionary)
    - pos_actual : is a :class:`pydevmgr.UaNode`  
    
    Args:
        key (str): The string key representing the node in its context.
                   If key='a.b.c'  'a.b' is the `prefix` and 'c' the `name` of the node
        uacom_node (:class:`UaComNode`, :class:`opcua.Node`): The client com interface for OPC-UA 
        parser (callable, optional): A value parser for the set method (e.g. float, int, ...)
                This is handy for nodes representing a e.g. 16 bits integer on the server side.
                
                Several parser to ua Variant are defined in pydevmgr: 
                
                - Int16, INT    (INT is an alias as TwinCat defines it)
                - Int32, DINT
                - Int64, LINT
                - UInt16, UINT
                - UInt32, UDINT
                - UInt64, ULINT
                - Float, REAL
                - Double, LREAL
                
    Example:
    
    ::
      
        import pydevmgr
        import opcua
        
        client = opcua.client('url')
        current = pydevmgr.Node( 'current', client.get_node('ns=4;s=MAIN.lrCurrent') )
        substate =  pydevmgr.Node( 'substate', client.get_node('ns=4;s=MAIN.Motor1.stat.nSubstate'), parser=pydevmgr.INT )
             
    """
    
    def __init__(self,  
          key: str, 
          uacom_node: Union[UaComNode,opcua.Node],  
          parser: Optional[Callable] = None
        ) -> None:
        super().__init__(key, parser=parser)
        if isinstance(uacom_node, opcua.Node):
            uacom_node = UaComNode(uacom_node)
        
        self._uacom_node = uacom_node    
    
    @classmethod
    def new(cls, 
          parent: Any, 
          name: str, 
          ua_name : Optional[str] = None, 
          parser: Optional[Callable] = None, 
          namespace: Optional[int] = None
        ) -> BaseNode:
        """ Build a new :class:`UaNode` 
        
        The parent node shall have:
        
            - key attribute
            - _uacom attribute
            - join_uakey method 
            - ua_namespace attribute if namespace is None 
            - map attribute dictionary used if ua_name is None, then ua_name = parent.map[name] 
        
        Args:
            parent (any): mostlikely a :class:`UaInterface`
            name (str):  Node name 
            ua_name (optional , str): Node name in the UA server namespace.
                If not given ua_name = parent.map[name]
            parser (optional, callable): A value parser for the set method
            namespace (optional, int): namespace on the OPC-UA server side 
        
        """
        if not ua_name:
            ua_name = parent.map[name]
        if namespace is None:
            namespace = mconfig.namespace if parent.ua_namespace is None else parent.ua_namespace
        
        ua_id = "ns={};s={}".format(namespace, parent.join_uakey(ua_name))
        uacom_node = parent._uacom.get_node(ua_id)
        return cls( kjoin(parent.key, name), uacom_node, parser=parser)
    
    @property
    def prefix(self) -> str:
        return ksplit(self._key)[0]
            
    @property
    def name(self) -> str :
        return ksplit(self._key)[1]
    
    @property
    def sid(self) -> Any:
        return self._uacom_node.sid
    
    @property
    def uanodeid(self) -> ua.NodeId:
        return self._uacom_node.nodeid
        
    def read_collector(self) -> UAReadCollector:
        """ Return a :class:`UAReadCollector` object to queue nodes for reading """
        return self._uacom_node.read_collector()
    
    def write_collector(self) -> UAWriteCollector:
        """ Return a :class:`UAWriteCollector` object to queue nodes and values for writing """
        return self._uacom_node.write_collector()
    
    def fget(self) -> Any:
        """ get the value from server """
        return self._uacom_node.get_value()
    
    def fset(self, value: Any) -> None:
        """ set the value on server 
        
        Args:
            value (any): if :attr:`~UaNode.parser` is defined it is used to parse the value
                can be str, float, int, or :class:`ua.Variant` or  :class:`ua.DataValue` 
        """
        datavalue = self._parse_value_for_ua(value)
        self._uacom_node.set_value(datavalue)
            
    def _parse_value_for_ua(self, value: Any) -> None:        
        #if self._parser:
        #    value = self._parser(value)
        return self._uacom_node.parse_value(value)
        
