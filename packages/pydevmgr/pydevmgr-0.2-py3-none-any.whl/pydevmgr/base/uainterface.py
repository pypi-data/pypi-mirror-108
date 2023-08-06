from pydevmgr_core import BaseNode, BaseInterface
from .uacom import opcua, UaCom
from .uanode import UaNode
from .config import mconfig 

from typing import Optional, Any, Union, List, Type

class UaInterface(BaseInterface):
    """ Interface between opc-ua nodes and pydevmgr. This basically is set of :class:`Nodes` 
    
    Args:
        
        key (str): a unique key defining the interface. This is generally the same key as the host 
                  :class:`Device`. e.g. mgr.motor1.key ==  mgr.motor1.stat.key == mgr.motor1.cfg.key
        uacom (:class:`UaCom`, :class:`opcua.Client`, str): 
            - if str create a :class:`UaCom` from the str address 
            - if :class:`opcua.Client` wrap it in a :class:`UaCom`
            - if :class:`UaCom` use it
        map (dict): a dictionnary of name/node_suffix pairs 
            Like:     
            
                ::
                  
                    {'velocity' :     'cfg.lrDefaultVelocity',
                     'max_pos' :      'cfg.lrMaxPosition',
                     'min_pos' :      'cfg.lrMinPosition',
                     'check_inpos' :  'cfg.bCheckInPos', 
                     # etc...
                     }
        ua_prefix (str): The prefix for the OPC-UA path like for instance 'MAIN.Motor1.stat'
        ua_namespace (int, optional): 
            The ua name space default is defined in :obj:`mconfig.namespace` (4 by default)
    """
    _uacom = None
    _map = None
    _ua_prefix = None
    
    Node = UaNode    
    
    def __init__(self, 
          key: str, 
          uacom: Union[UaCom, opcua.Client], 
          map: dict, 
          ua_prefix: str, 
          ua_namespace: Optional[int] = None
        ) -> None:
        super().__init__(key)
        if isinstance(uacom, opcua.Client):
            uacom = UaCom(ua_client=uacom)
        elif isinstance( uacom, str):
            uacom = UaCom(address=uacom)
        
        self._uacom = uacom
        self._map = map

        self._ua_prefix = ua_prefix        
        self._ua_namespace = mconfig.namespace if ua_namespace is None else ua_namespace
    
    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            try:
                return self.get_node(attr)
            except KeyError:
                raise AttributeError(attr)

    @classmethod
    def new(cls, 
          parent: Any, 
          name: str, 
          map: Optional[dict] = None, 
          namespace: Optional[int] = None
        ):
        """ Create an :class:`UaInterface` from a parent object 
        
        The parent is most likely a :class:`pydevmgr.UaDevice` object. 
        The parent shoudl have: 
          - .map attribute if ``map`` args is None
          - .namespace attribute if ```namespace`` args is None
          - ._uacom attribute 
          - .join_uakey() method 
          
        Args:
            parent (Any):  most likely a :class:`pydevmgr.UaDevice` object. 
            name (str): e.g. 'stat', 'cfg'. name is use only to retrieve the map information from 
                the parent.map dictionary if `map` is given this is ignored. e.g. 'stat', 'cfg'
            map (optional, dict, None): if None extract it from parent with the given ``name`` 
            namespace (optional, int, None): if None extract it from parent     
        """
        if map is None:
            map = parent.map.get(name, {})
        if namespace is None:
            namespace = parent.ua_namespace
        # The name is not added to the parent key here 
        return cls( parent.key, parent._uacom, map, parent.join_uakey(), ua_namespace=namespace)
    
    @property
    def prefix(self):        
        return self.split_key(self._key)[0]
        
    @property
    def name(self):
        return self.split_key(self._key)[1]
    
    @property
    def map(self):
        return self._map
    
    @property
    def ua_prefix(self):
        return self._ua_prefix
    
    @property
    def ua_namespace(self):
        return self._ua_namespace
    
    def join_uakey(self, *names) -> str:        
        names = (self._ua_prefix,)+names
        return ".".join(a for a in names if a)
    
    @classmethod
    def _get_vtype(cl, name) -> Type:
        return None 
        """ look in class __annotations__ to find any vtype for a given name """
        
        for subcl in cl.__mro__:
            try:
                return subcl.__annotations__[name]
            except (KeyError,AttributeError):
                continue
        return None
    
    @property
    def all_native_nodes(self) -> List:
        """ return a list nodes of the interface 
        
        ..seealso::
        
           :attr:`UaInterface.~all_nodes`
           :meth:`UaInterface.~get_nodes`
        """
        return [self.get_node(k) for k in self.map.keys()]
    
    @property
    def all_nodes(self) -> List:
        """ return a list of all nodes (including aliases) of the interface 
        
        ..seealso::
        
           :attr:`UaInterface.~all_native_nodes`
           :meth:`UaInterface.~get_nodes`
        """
        _ = self.all_native_nodes # make sure all native nodes are cashed 
        self._cash_all()
        return [v for v in self.__dict__.values() if isinstance(v, (BaseNode))]       
        
    def get_nodes(self, node_names: Optional[List[str]] = None) -> List[BaseNode]:
        """ return a list of :class:`Node` from a list of names 
        
        if node_names is None all the nodes (inluding aliases) are return. 
        If one want only the "native" nodes use the ``.all_native_nodes`` property
        
        Args:
            node_names (optional, list of str): list of node names 
        
        !!! Warning if a given name startwith '_' this method may return something which is not 
           a :class:`Node` or :class:`NodeAlias`. No check is done for performance raison.  
        """
        if node_names is None:
            return self.all_nodes
        return [self.get_node(n) for n in node_names]
    
    def get_node(self, name : str) -> BaseNode:
        """ Return a Node for the given key

        Args:
           name (str): node name 
        
        !!! Warning if the given name startwith '_' this method may return something which is not 
           a :class:`Node`. No check is done for performance raison.  

        Exemple:
        
            > pos = motor1.stat.get_node('pos_actual')
            Is equivalent to
            > pos = motor1.stat.pos_actual
            
            Then one can do
            > print( "position:", pos.get() )
        """
        try:
            node = self.__dict__[name]
        except KeyError:
            try:
                node = object.__getattribute__(self, name)
            except AttributeError:
                node = self.Node.new(self, name)
            self.__dict__[name] = node            
        return node    
    
