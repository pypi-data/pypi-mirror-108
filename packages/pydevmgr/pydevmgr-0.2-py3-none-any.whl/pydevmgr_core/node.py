from .base import _BaseObject, _BaseProperty, ksplit, kjoin, join_key
import weakref
from typing import Dict, Any, Optional

class BaseReadCollector:
    """ The Read Collector shall collect all nodes having the same sid and read them in one call
    
    - __init__ : should not take any argument 
    - add : take one argument, the Node. Should add node in the read queue 
    - read : takes a dictionary as arguement, read the nodes and feed the data dict according to node keys 
    
    The BaseReadCollector is just a dummy implementation where nodes are red one after the other     
    """
    def __init__(self):
        self._nodes = set()
    def add(self, node):
        self._nodes.add(node)
    def read(self, data):
        for node in self._nodes:
            data[node] = node.get()

class BaseWriteCollector:
    """ The Write Collector shall collect all nodes having the same sid, its value, and write them in one call
    
    - __init__ : should not take any argument 
    - add : take two argument, the Node and its value attached. Should add node,value in the write queue 
    - write  : takes no arguement, write the node/value 
    
    The BaseWriteCollector is just a dummy implementation where nodes are written one after the other  
    """
    
    def __init__(self):
        self._nodes = {}
    
    def add(self, node, value):
        self._nodes[node] = value
    
    def write(self):
        for node, val  in self._nodes.items():
            node.set(val)

class DictReadCollector:
    """ A collector to read from a dictionary instead of getting node from server 
    
    Design to be used as simulator
    """
    def __init__(self, data):
        self._data = data
        self._nodes = set()
        
    def add(self, node):
        self._nodes.add(node)

    def read(self, data):
        for node in self._nodes:
            data[node] = self._data[node.key]

class DictWriteCollector:
    """ A collector to write to a dictionary instead of setting node to server """
    def __init__(self, data):
        self._data = data
        self._nodes = {}
        
    def add(self, node, value):
        self._nodes[node] = value
        
    def write(self):
        for node, val  in self._nodes.items():
            self._data[node.key] = val
                

class BaseNode(_BaseObject):
    """ This a base class defining the base methods for a node 
    
    The requirement for a Node is to have: 
        - a .key (str) attribute
        - a .sid (any hashable) attribute (iddenify an id to group nodes together for efficient reading and writting 
            in one server call). If sid is None the node is threated of an "alias Node".
            The only requirement for sid is that it should be hashable.
        - a .get(data=None) method 
        - a .set(value, data=None) method 
        - read_collector() : a constructor for a node collector for reading 
        - write_collector() : a constructor for a node collector for writting
    
    To implement from BaseNode one need to implement the .fget and .fset method (they are called by .get and .set)
                     
    __init__ must have the key argument and any optional other arguments specific to the node and its communication
    
    """
    def __init__(self, key, parser=None):
        super().__init__(key)
        self._parser = parser
        
    @property
    def sid(self):
        """ default id server is 0 
        
        The sid property shall be adujsted according to read_collector and write_collector methods 
        """
        return 0
    
    @property
    def parser(self):
        return self._parser
    
    @classmethod
    def prop(this_cls, name, *args, **kwargs):
        """ A class method use to define a Node property 
        
        This should be used inside a class definition. 
        The property define a place holder for the node creation, it can hold some parameters of the 
        future nodes object created within its parent context. The creation of the node can than be 
        a mix of static and dynamical argument. 
         
        The node is created on the parent object the first time the attribute is reached and than 
        it is cashed inside the parent object __dict__. 
        
        
        Example:
        
        ::
        
            from pydevmgr_core import BaseNode, BaseInterface, download
            
            class SimCom:
                " simulate a communication "
                def __init__(self):
                    self._channels = {0: 18.5, 1: 2.3}
                    
                def get_value_from_channel(self, channel):
                    return self._channels[channel]
        
            class MyNode(BaseNode):
                def __init__(self, key, com, channel=0):
                    super().__init__(key)
                    self._com = com 
                    self._channel = channel
                
                @classmethod
                def new(cls, parent, name, channel=0):
                    return cls(parent.key + "." + name, parent._com, channel)
                
                def fget(self):
                    return self._com.get_value_from_channel(self._channel)
                    
            class MyInterface(BaseInterface):
                def __init__(self, key , com):
                    super().__init__(key)
                    self._com = com 
                
                temp = MyNode.prop('temp', channel=0)
                pressure = MyNode.prop('pressure', channel=1)
            
            >>> env =  MyInterface('env', SimCom())
            >>> env.temp.get()
            18.5
            >>> d = {}; download( [env.temp, env.pressure], d)
            >>> d
            {'env.temp': 18.5, 'env.pressure': 2.3}
                   
        """
        kwargs.setdefault('cls', this_cls)
        return NodeProperty(name, *args, **kwargs)
    
    def read_collector(self) -> BaseReadCollector:
        """ return a collector of nodes for readding 
        
        This is used to collect all nodes with the same sid. 
        The result is done in one call per server when ever it is possible. 
        
        The returned object must have:
            a  ``.add(node)`` method 
            a  ``.read(data)`` method 
        
        The BaseReadCollector is however gettting the node value one by one. The method has to be 
        implemented for other Nodes
        """
        return BaseReadCollector()
    
    def write_collector(self) -> BaseWriteCollector:
        """ return a collector of nodes for writting
        
        This is used to collect all nodes with the same sid. All node could be written in one call
        on the server. 
        
        The returned object must have:
            a  ``.add(node, value)`` method 
            a  ``.write()`` method 
        
        The BaseWriteCollector is however setting the node value one by one. The method has to be 
        implemented for other Nodes
        """
        return BaseWriteCollector()
            
    def get(self, data: Dict =None) -> Any:
        """ get value of the data Node 
        
        If the optional data dictionary is given data[self] is return otherwise self.fget() is returned
        fget() will fetch the value from a distant server for instance (OPC-UA, Websocket, OLDB, etc ...)
        
        """
        if data is None:
            return self.fget()
        return data[self]
    
    
    def set(self, value, data=None):
        """ Set node value 
        
        If the optional data dictionary is given `data[self] = value`, otherwise  self.fset(value) is used 
        """
        if self._parser:
            value = self._parser(value)
        
        if data is None:
            self.fset(value)
        else:
            data[self] = value
    
    ### ############################################
    #
    # To be implemented by the child class  
    #
    
    def fget(self):
        """ This is the function we need to implement to get real data """
        raise NotImplementedError('fget')
    
    def fset(self, value):
        """ This is the function we need to implement to set real data """
        raise NotImplementedError('fset')
    
    # To be implemented 
    #@classmethod
    #def new(cls, parent, ....)    

        
class NodeAlias(BaseNode):
    """ NodeAlias mimic a real client Node. 
        
    The NodeAlias object does a little bit of computation to return a value with its `get()` method and 
    thanks to required input nodes.
     
    The NodeAlias cannot be use as such without implementing a `fget` method. This can be done by 
    implementing the fget method on the class or with the `nodealias` decorator. 
    
    NodeAlias is an abstraction layer, it does not do anything complex but allows uniformity among ways to retrieve values. 
    
    NodeAlias object can be easely created with the @nodealias() decorator
    
    Args:
        key (str): Key of the node
        nodes (list, class:`BaseNode`): list of nodes necessary for the alias node. When the 
                     node alias is used in a Downloader object, the Downloader will automaticaly fetch 
                     those required nodes from server (or orher node alias).
                     
    Example: 
    
    ::
    
        >>> is_inpos_for_test = NodeAlias('is_inpos_for_test', [mgr.motor1.stat.pos_actual])
        >>> is_inpos_for_test.fget = lambda pos: abs(pos-4.56)<0.01
        >>> is_inpos_for_test.get()
    
    :: 
    
        @nodealias("is_all_standstill", [mgr.motor1.stat.substate, mgr.motor2.stat.substate])
        def is_all_standstill(m1_substate, m2_substate):
            return m1_substate == Motor.SUBSTATE.OP_STANDSTILL and m2_substate == Motor.SUBSTATE.OP_STANDSTILL
    
        >>> is_all_standstill.get()
        True
        
        >>> downloader = Downloader( [is_all_standstill] )
        >>> downloader.download()        
        >>> downloader.get_data()
        {'fcs.motor1.substate': 100,
         'fcs.motor2.substate': 100,
         'is_all_standstill': False}
         
    In the exemple above one can see that the mgr.motor[12].stat.substate has been automatically added 
    to the nodes to be fetched from OPC-UA server(s). 
    
    Here is an exemple of customized NodeAlias
    
    ::
    
        import numpy as np 
        
        class MinMaxNode(NodeAlias):
            min = +np.inf
            max = -np.inf
            
            def fget(self, pos):
                self.min = min(pos, self.min)
                self.max = max(pos, self.max)
                return ( self.min , self.max )
            
            def reset(self):
                self.min = +np.inf
                self.max = -np.inf
                
        mot1_minmax = MinMaxNode( "minmax",  [mgr.motor1.stat.pos_actual])
                
    .. seealso::  
        :func:`nodealias`
        :func:`nodealiasproperty`
        :class:`NodeAlias`            
    """
    def __init__(self, key, nodes):
        super().__init__(key)
        if isinstance(nodes, BaseNode):
            nodes = [nodes]
        self._nodes = nodes
        
    @property
    def sid(self):
        """ sid of aliases must return None """ 
        return None
    
    @property
    def nodes(self):
        return self._nodes
    
    @classmethod
    def new(cls, parent, name, node_names, *args, **kwargs):
        """ a base constructor for a NodeAlias within a parent context  
        
        The requirement for the parent :
            - a .key attribute 
            - attribute of the given name in the list shall return a node
        """
        if isinstance(node_names, str):
            node_names = [node_names]
        
        nodes = []
        for n in node_names:
            if isinstance(n, str):
                node = getattr(parent, n)
                if not isinstance(node, BaseNode):
                    raise ValueError("Attribute {!r} of parent is not a base node got a {}".format(n , type(node)))
                nodes.append(node)
            elif isinstance(n, BaseNode):
                nodes.append(n)
            elif isinstance(n, tuple):
                cparent = parent
                for sn in n[:-1]:
                    cparent = getattr(cparent, sn)
                node = getattr(cparent, n[-1])
                if not isinstance(node, BaseNode):
                    raise ValueError("Attribute {!r} of parent is not a base node got a {}".format(n , type(node)))
                nodes.append(node)
            else:
                raise ValueError('node shall be a parent attribute name, a tuple or a BaseNode got a {}'.format(type(n)))
        
        return cls(join_key(parent, name), nodes, *args, **kwargs)
    
    @classmethod
    def prop(this_cls, name, *args, **kwargs):
        kwargs.setdefault('cls', this_cls)
        return NodeProperty(name, *args, **kwargs)
        
    def get(self, data: Optional[Dict] =None) -> Any:
        """ get the node alias value from server or from data dictionary if given """
        if data is None:
            _n_data = {}
            NodesReader(self._nodes).read(_n_data)
            values = [_n_data[n] for n in self._nodes]
            #values = [n.get() for n in self._nodes]
        else:
            values = [data[n] for n in self._nodes]
        return self.fget(*values)
    
    def set(self, value: Any, data: Optional[Dict] =None) -> None:
        """ set the node alias value to server or to data dictionary if given """
        values = self.fset(value)
        if data is None:
            NodesWriter(dict(zip(self._nodes, values))).write()                        
            #for n,v in zip(self._nodes, values):
            #    n.set(v)
        else:
            for n,v in zip(self._nodes, values):
                data[n] = v        
    
    def fget(self, *args) -> Any:
        """ This is the function we need to implement to get real data 
        
        The number of argument must match the number of nodes
        """
        raise NotImplementedError('fget')
    
    def fset(self, value) -> None:
        """ This is the function we need to implement to set real data
         
        The number of returned value must match the number of nodes 
        """
        raise NotImplementedError('fset')    



class NodeProperty(_BaseProperty):
    _cls = None#"Node"
    _constructor = None
    
    fget = None
    fset = None
    
    def getter(self, func):
        """ decoraotr to define the fget function """
        self.fget = func
        return self # must return self
    
    def setter(self, func):
        """ decoraotr to define the fset function """
        self.fset = func    
        return self # must return self
    
    def _finalise(self, parent, node):
        # overwrite the fget, fset function to the node if defined 
        parent_wr = weakref.ref(parent)
        if self.fget:            
            def fget(*args, **kwargs):
                return self.fget(parent_wr(), *args, **kwargs)
            node.fget = fget
        if self.fset:
            def fset(*args, **kwargs):
                return self.fset(parent_wr(), *args, **kwargs)
            node.fset = fset
    
    def __call__(self, func):
        """ The call is used has fget decorator """
        self.fget = func
        return self

def nodeproperty(name,  *args, **kwargs):
    """ A decorator for a quick node creation 
    
    This shall be implemented in a parent interface or any class 
    
    Args:
        name (str) : name of the node. The key of the node will be parent_key.name
        cls (class, optional): default is :class:`BaseNode` used to build the node  
        \*args, \*\*kwargs: All other arguments necessary for the node construction
    """
    return BaseNode.prop(name, *args, **kwargs)

def nodealiasproperty(name, nodes, *args, **kwargs):
    """ A decorator for a quick alias node creation 
    
    This shall be implemented in a parent interface or any class with the ``get_node`` method
    
    Args:
        name (str) : name of the node. The key of the node will be parent_key.name
        cls (class, optional): default is :class:`NodeAlias` used to build the node  
        \*args, \**kwargs: All other arguments necessary for the node construction this is only used 
                         if an laternative cls is given 
    """
    return NodeAlias.prop(name, nodes, *args, **kwargs)

def node(key):
    """ This is a node decorator 
    
    This allow to quickly embed any function in a node without having to subclass Node
    
    The build node will be readonly, for a more complex behavior please subclass a BaseNode
    
    Args:
        key (str): string key of the node
    
    Returns:
       func_setter: a decorator for the fget method  
       
    Example:
    
    A simulator of value:
    
    ::
        
        @node('temperature')
        def temperature():
            return np.random.random()*3 + 20
        
        temperature.get()
        
    Node returning the local float time in seconds 
    
    :: 
        
        @node('local_time')
        def local_time():
            return time.time()
    """
    node = BaseNode(key)
    def set_fget(func):
        node.fget = func
        if hasattr(func, "__func__"):
            node.__doc__= func.__func__.__doc__
        else:
            node.__doc__ = func.__doc__
        return node
    return set_fget

def nodealias(key, nodes):
    """ This is a node alias decorator 
    
    This allow to quickly embed any function in a node without having to subclass the Alias Node
    
    The build node will be readonly, for a more complex behavior please subclass an NodeAlias
    
    Args:
        key (str): string key of the node
        nodes (lst): list of nodes 
        
    Returns:
       func_setter: a decorator for the fget method  
       
    Example:
    
    A simulator of value:
    
    ::
        
        @node('temperature_volt')
        def temperature_volt():
            return np.random.random()*3 + 20
        
        @aliasnode('scaled_temperature', [temperature_volt]):
        def scaled_temperature(temp):
            return temp*10 
    """
    node = NodeAlias(key,nodes)
    def set_fget(func):
        node.fget = func
        if hasattr(func, "__func__"):
            node.__doc__= func.__func__.__doc__
        else:
            node.__doc__ = func.__doc__
        return node
    return set_fget


def setitem(obj,k,v):
    obj[k] = v

class NodesReader:
    def __init__(self, nodes=tuple()):
        self._input_nodes = nodes # need to save to remenber the order
        self._dispatch, self._aliases = {}, []
        for node in nodes:
            self.add(node) 
            
    def add(self, node):
        # if no _sid, this ia an alias or a standalone node and should be call 
        # at the end
        
        # None object are ignored 
        if node is None:
            return 
                
        if isinstance(node, (tuple, list, set)):
            for n in node:
                self.add(n)
         
        sid = getattr(node, 'sid', None)
        if sid is None:
            self._aliases.append( node )
            for n in getattr(node, "nodes", []):            
                self.add(n)
            return         
        try:
            collection = self._dispatch[sid]
        except KeyError:
            collection = node.read_collector()
            self._dispatch[sid] = collection
        collection.add(node)
    
    def clear(self):
        self._dispatch.clear()
        self._aliases.clear()
    
    def read(self, data=None):
        """ read all node values 
        
        nodes are first grouped by sid and are red in one call is the server allows it 
        """
        # starts with the UA nodes 
        
        # :TODO: At some point, this should be asynchrone 
        for sid, collection in self._dispatch.items(): 
            collection.read(data)       
                
        # aliases are treated at the end, data should have all necessary real nodes for 
        # the alias 
        # We need to start from the last as Aliases at with lower index can depend 
        # of aliases with higher index
        aliases = self._aliases
        flags = [False]*len(aliases)
        for i, alias in reversed(list(enumerate(aliases))):
            if not flags[i]: 
                data[alias] = alias.get(data)                       
                flags[i]= True

class NodesWriter:
    def __init__(self, node_values):
        
        self._dispatch = {}
        
        # start with aliases, returned values are set inside 
        # the node_values dictionary
        for node, value in node_values.items():
            sid = getattr(node, 'sid', None)
            if sid is None:
                node.set(value, node_values)
        
        for node, value in node_values.items():
            sid = getattr(node, 'sid', None)
            if sid is not None:
                self.add(node, value)
    
    def clear(self):
        self._dispatch.clear()
        self._node_by_key.clear()
        
    def add(self, node, value):
        try:
            collection = self._dispatch[node.sid]
            
        except KeyError:
            collection = node.write_collector()
            self._dispatch[node.sid] = collection
        
        collection.add(node, value)
        
    def write(self) -> None:                
        # :TODO: At some point, this should be asynchrone 
        for collection in  self._dispatch.values():
            collection.write()
            

