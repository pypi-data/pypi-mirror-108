from pydevmgr_core import BaseRpc, ksplit, kjoin
from .uacom import UaComNode
from .tools import enum_txt, EnumTool
from .config import mconfig 

from enum import Enum
import opcua
from opcua import ua

from typing import Callable, Optional, Any, Tuple    


class RPC_ERROR(EnumTool, int, Enum):
    OK =  0
    NOT_OP =  -1
    NOT_NOTOP_READY =  -2
    NOT_NOTOP_NOTREADY = -3
    LOCAL =  -4
    
    UNREGISTERED = -9999 
    # etc ...
enum_txt( {
    RPC_ERROR.OK:					 'OK',
    RPC_ERROR.NOT_OP:				 'Cannot control motor. Not in OP state.',
    RPC_ERROR.NOT_NOTOP_READY:	     'Call failed. Not in NOTOP_READY.',
    RPC_ERROR.NOT_NOTOP_NOTREADY:	 'Call failed. Not in NOTOP_NOTREADY/ERROR.',
    RPC_ERROR.LOCAL:				 'RPC calls not allowed in Local mode.',
    RPC_ERROR.UNREGISTERED:			 'Unregistered RPC Error',
    # etc 
})

class UaRpc(BaseRpc):
    """ Object representing an OPC-UA Rpc method 

    It does the interce beetween a python method and the OPC-UA method
    
    Both methods  :func:`RpcNode.call` and :func:`RpcNode.rcall` are calling the server Rpc. 
    The first one is returning an rpc_error code, the second return nothing but raise an :class:`RpcError` 
    exception in case of error.
    
    In rare case user will use the RpcNode as it is automatically created from :class:`RpcInterface` containing 
    all the mapping. The rpc's are mostlikely called from the device methods. 
    
    Args:
        key (str): shall be unic in its context. This is for compatibility reason, this is not relevant for methods
        ua_node (:class:`UaComNode`, :class:`opcua.Node`): a com clien tobject to the OPC-UA server
                   !! This is the node of the OPC-UA structure containing the method
                   
        ua_method_id(str): The ua method id
        args_parser (None, iterable, optional): a list of callable parser for the method arguments. 
                If given the number of `args_parser` shall match the number of arguments in the server 
                Rpc Method (no check is done).
                
    
    Example:
        
    ::
        
        import opcua 
        from pydevmgr_elt import RpcNode
        
        client = opcua.Client('..url..')
        move_abs = UaRpcNode('mot1.move_abs', client.get_node('ns=4;s=MAIN.Motor1'), '4:RPC_MoveAbs', args_parser=(float, float))         
    
    """
    RPC_ERROR = RPC_ERROR
    def __init__(self, 
          key: str, 
          uacom_node: UaComNode, 
          ua_method_id: str, 
          args_parser: Optional[Tuple[Callable]] = None,           
          RPC_ERROR: RPC_ERROR = None
        ):
        super().__init__(key, args_parser=args_parser)
        if isinstance(uacom_node, opcua.Node):
            uacom_node = UaComNode(uacom_node)
        self._uacom_node = uacom_node
        self._ua_method_id = ua_method_id
        # redefine the RPC_ERROR constants dynamicaly 
        if RPC_ERROR:
            self.RPC_ERROR = RPC_ERROR
        
    @classmethod
    def new(cls, 
          parent: Any, 
          name: str, 
          ua_method_name: Optional[str] = None, 
          args_parser: Optional[Tuple[Callable]] =None, 
          namespace: Optional[int] = None, 
          RPC_ERROR: RPC_ERROR = None
        ):
        """ Build a new child UaRpc from a parent (mostlikely a :class:`pydevmgr.UaRpcInterface`)
        
        The parent node shall have:
        
            - key attribute
            - _uacom attribute
            - ua_prefix attribute 
            - ua_namespace attribute is namespace is None
            - map attribute (dictionary) if ua_method_name is None 
        
        And optionaly 
            
            - RPC_ERROR: Enum for rpc errors
            
        Args:
            parent (any): mostlikely a :class:`pydevmgr.UaRpcInterface`
            name (str): name of the method in the python name sapec and as defined in the parent.map
            ua_method_name (str, optional): OPC-UA method name if None then ``ua_method_name = parent.map[name]``
            args_parser (iterable, optional): A list of parsers for the method arguments. 
                 If None, ``args_parser = parent._get_args_parser(name)``  if _get_args_parser method exists in parent 
                 
            namespace (int, optional): namespace, if None, ``namespace = parent.us_namespace``
            RPC_ERROR (Enum, optional): Enumerator of (EnumTool, int). If None ``RPC_ERROR = parent.RPC_ERROR``
        
        """
        if not ua_method_name:
            ua_method_name = parent.map[name]
        if namespace is None:
            namespace = mconfig.namespace if parent.ua_namespace is None else parent.ua_namespace            
        if RPC_ERROR is None:        
            RPC_ERROR = getattr(parent, "RPC_ERROR", None)
        #if args_parser is None and hasattr(parent, "_get_args_parser"):
        #    args_parser = parent._get_args_parser(name)
            
        #if args_parser is None:
        #    args_parser = parent._get_args_parser(name)
        
        # get the parent node of the method
        ua_id = "ns={};s={}".format(namespace, parent.ua_prefix)
        uacom_node = parent._uacom.get_node(ua_id)
        ua_method_id = "{}:{}".format(namespace, ua_method_name)        
        return cls( kjoin(parent.key, name), uacom_node, ua_method_id, args_parser=args_parser, RPC_ERROR=RPC_ERROR)
    
    @property
    def key(self) -> str:
        return self._key
    
    @property
    def prefix(self) -> str:
        return ksplit(self._key)[0]
        
    @property
    def name(self) -> str:
        return ksplit(self._key)[1]
    
    @property
    def sid(self) -> str:
        """ not use yet but here for future integration """
        return self._uacom_node.sid
    
    @property
    def uanodeid(self) -> ua.NodeId:
        return self._uacom_node.nodeid
    
    def get_error_txt(self, rpc_error: int) -> str:
        """ get a text description of the rpc_error code 
        
        See the enumerator RPC_ERROR attribute 
        
        Args:
            rpc_error (int): rpc error code  
        """
        return self.RPC_ERROR(rpc_error).txt
    
    def fcall(self, *args) -> int:
        """ call method on serser, the arguments has been parsed before """
        return self._uacom_node.call_method(self._ua_method_id, *args)
