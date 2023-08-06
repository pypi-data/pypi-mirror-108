from pydevmgr_core import kjoin, ksplit, BaseInterface
from .uacom import opcua, UaCom
from .uarpc import UaRpc, RPC_ERROR
from .config import mconfig 
from typing import Callable, Optional, Any, Type, Union

class UaRpcInterface(BaseInterface):
    """ Interface pydevmgr/OPC-UA which handle several :class:`RpcNodes` 
    
    Args:
        
        key (str): a unique key defining the interface. This is generally the same key as the host 
                  :class:`Device`. e.g. mgr.motor1.key ==  mgr.motor1.rpc.key
                  key for rpc method interface is not as relevent as for :class:`Interface`
        ua_client (UaCom, opcua.Client): opcua client connected to some servers
        map (dict): a dictionnary of name/rpc_node pairs 
            Like:     
            
                ::
                  
                    {   'rpcInit'    : 'RPC_Init',
                        'rpcEnable'  : 'RPC_Enable',
                        'rpcDisable' : 'RPC_Disable',
                    # etc ...
                    }
                    
        ua_prefix (str): The prefix for the OPC-UA path like for instance 'MAIN.Motor1'
        ua_namespace (int,str, optional): The ua name space default is 4
        
    """
    _uacom = None
    _map = None
    _ua_prefix = None
    
    RpcNode = UaRpc
    RPC_ERROR = RPC_ERROR
    
    def __init__(self, 
          key: str, 
          uacom: Union[UaCom, opcua.Client], 
          map: dict, 
          ua_prefix: str, 
          ua_namespace: Optional[int] = None, 
          RPC_ERROR: Type[RPC_ERROR] = None
        ):
        super().__init__(key)
        if isinstance(uacom, opcua.Client):
            uacom = UaCom(ua_client=uacom)
        
        self._uacom = uacom
        self._map = map
        
        self._ua_prefix = ua_prefix
        
        self._ua_namespace = mconfig.namespace if ua_namespace is None else ua_namespace
        
        # redefine the RPC_ERROR dynamicaly 
        if RPC_ERROR:
            self.RPC_ERROR = RPC_ERROR
        
    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            try:
                return self.get_method(attr)
            except KeyError:
                raise AttributeError(attr)
    
    
    @classmethod
    def new(cls, 
          parent: Any, 
          name: str, 
          map: Optional[dict] = None, 
          namespace: Optional[int] = None, 
          RPC_ERROR: Type[RPC_ERROR] = None
        ):
        """ Create an :class:`UaRpcInterface` from a parent object 
        
        The parent is most likely a :class:`pydevmgr.UaDevice` object. 
        The parent shoudl have: 
          - .map attribute if ``map`` argument is None
          - .namespace attribute if ```namespace`` argument is None
          - ._uacom attribute 
         
          
        Args:
            parent (Any):  most likely a :class:`pydevmgr.UaDevice` object. 
            name (str):  e.g. 'rpc'. name is use only to retrieve the map information from 
                the parent.map dictionary if `map` is given this is ignored.
            map (optional, dict, None): if None extract it from parent with the given ``name`` 
            namespace (optional, int, None): if None extract it from parent     
        """
        if map is None:
            map = parent.map[name]
        if namespace is None:
            namespace = parent.ua_namespace
        # The name is not added to the parent key here 
        return cls( parent.key, parent._uacom, map, parent.ua_prefix, ua_namespace=namespace, RPC_ERROR=RPC_ERROR)
    
    
    @classmethod
    def _get_atypes(cl, key):
        """ look in class __annotations__ to find any parser for a given key """
        return None
        
        for subcl in cl.__mro__:
            try:
                return subcl.__annotations__[key]
            except (KeyError,AttributeError):
                continue
        return None    
    
    @property
    def prefix(self) -> str:
        return ksplit(self._key)[0]

    
    @property
    def name(self) -> str:
        return ksplit(self._key)[1]    
    
    @property
    def map(self) -> dict:
        return self._map
        
    @property
    def ua_prefix(self) -> str:
        return self._ua_prefix
    
    @property
    def ua_namespace(self) -> int:
        return self._ua_namespace
    
    def get_method(self, name: str) -> UaRpc:
        """ get a rpc method object :class:`UaRpc`
        
        Args:
            name (str): name of the rpc method
        
        !!! Warning if the given name startwith '_' this method may return something which is not a :class:`RpcNode`. No check is done.    
        """        
        try:
            m = self.__dict__[name]
        except KeyError:
            try:
                m = object.__getattribute__(self, name)
            except AttributeError:
                m = self.RpcNode.new(self, name)
            self.__dict__[name] = m
        return m
