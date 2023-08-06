from .node import  BaseNode, NodeAlias
from collections import deque
import time
from  datetime import datetime, timedelta
from typing import Union, List, Dict, Optional

__all__ = [
"UnixTimeNode",
"LocalTimeNode",
"LocalUtcNode", 
"DequeNode", 
"local_utc", 
"local_utc2", 
"local_time",
"AllTrue", 
"AllFalse", 
"AnyTrue", 
"AnyFalse", 
"InsideIntervalNode", 
"PosNameNode"
]


class UnixTimeNode(BaseNode):
    """ A basic node returning the float local time  
    
    Args:
        key (str): node key
        delta (float): time shift in seconds 
        
    Properties:
        _delta : the _delta timeshift in second 
    """
    def __init__(self, key: str = 'local_time', delta : float = 0):
        super().__init__(key)
        self._delta = delta
    
    def fget(self) -> float:
        return time.time()+self._delta 

class LocalTimeNode(BaseNode):
    """ A basic node returning the float local time  
    
    Args:
        key (str): node key
        delta (float): time shift in seconds 
        
    Properties:
        _delta : the _delta timeshift in second 
    """
    def __init__(self, key: str = 'local_time', delta : float = 0):
        super().__init__(key)
        if not isinstance(delta, timedelta):
            delta = timedelta(seconds=delta)
        self._delta = delta
    
    def fget(self) -> float:
        return datetime.now()+self._delta
        

local_time = LocalTimeNode('local_time', 0)

class LocalUtcNode(BaseNode):
    """ A basic node returning the local UTC as string 
    
    Args:
        key (str): node key
        delta (float, optional): time shift in seconds 
        format (str, optional): Returned format, default is iso 8601 '%Y-%m-%dT%H:%M:%S.%f%z'
    Properties:
        _delta : the _delta timeshift in second 
    """
    def __init__(self, key : str ='local_utc', delta: float =0, format: str ='%Y-%m-%dT%H:%M:%S.%f%z'):
        super().__init__(key)
        self._delta = delta
        self._format = format
        
    def fget(self) -> str:
        tc = datetime.utcnow()+timedelta(seconds=self._delta)   
        return tc.strftime(self._format)
        
##
# Add an instance to the local_utc 
local_utc  = LocalUtcNode('local_utc', 0)
local_utc2 = LocalUtcNode('local_utc', 0, '%Y-%m-%d-%H:%M:%S.%f%z')


class DequeNode(NodeAlias):
    """ This is an :class:`NodeAlias` returning at each get a :class:`collections.deque` 
    
    Specially handy for live plot and scopes
    
    Args:
       key (string): alias node keyword 
       nodes (list of :class:`UaNode`,:class:`NodeAlias`): 
              List of nodes to get()  
       maxlen (int): maximum len of the dequeu object  
    
    Example:
        
    In this example the first motor is moving while the second standstill at 0.0
         
    ::
    
        >>> from pydevmgr_core import local_time
        >>> time = UnixTimeNode('time') 
        >>> nodes = [time, mgr.motor1.stat.pos_actual, mgr.motor2.stat.pos_actual]
        >>> f = DequeNode( "mot_poses", nodes, 20)
        >>> f.get()
        deque([(1604931613.136023, 96.44508185106795, 0.0)])
        >>> f.get()
        deque([(1604931613.136023, 96.44508185106795, 0.0),
        (1604931614.258859, 95.32508185106808, 0.0)])
        >>> f.get()
        deque([(1604931613.136023, 96.44508185106795, 0.0),
        (1604931614.258859, 95.32508185106808, 0.0),
        (1604931615.451603, 94.13508185106821, 0.0)])
        >>> etc ....
        
    """
    def __init__(self, 
          key: str, 
          nodes: Union[BaseNode,List[BaseNode]], 
          maxlen: int = 100, 
          trigger_index: Optional[int] = None
        ) -> None: 
            
        super().__init__(key, nodes)        
        
        self._data = deque([], maxlen)
        self._scalar = not hasattr(nodes, "__iter__")
                
        self._trigger_index = trigger_index
        
    @property
    def data(self):
        return self._data 
    
    @property
    def columns(self):
        return [n.key for n in self.nodes]
    
        
    def fget(self, *values): 
        if self._trigger_index is not None and not values[self._trigger_index]:
            return self._data      
        
        if self._scalar:
            self._data.append(values[0])
        else:
            self._data.append(values)
        return self._data
    
    def clear(self, maxlen=None):
        if maxlen is None:
            self._data.clear()
        else:
            self.maxlen = maxlen
            self._data = deque([], maxlen)

class AllTrue(NodeAlias):
    def fget(*nodes):
        return all(nodes)

class AnyTrue(NodeAlias):
    def fget(*nodes):
        return any(nodes)
        
class AllFalse(NodeAlias):
    def fget(*nodes):
        return not any(nodes)

class AnyFalse(NodeAlias):
    def fget(*nodes):
        return not all(nodes)

class InsideIntervalNode(NodeAlias):
    """ Bool Node alias to check if a value is inside a given position 
    
    Args:
        key (str):  node key
        node (:class:`BaseNode`): node returning a float like a position
        min (float, optional): min value of the interval 
        max (float, optional): max value of the interval
    """
    def __init__(self, key: str, node: BaseNode, min :float =None, max: float =None): 
        super().__init__(key, node)
        self.min = min
        self.max = max
         
    def fget(self, value):
        if self.fmin is not None and value<self.fmin:
            return False
        if self.fmax is not None and value>self.fmax:
            return False
        return True    

class InsideCircleNode(NodeAlias):
    """ Bool Node alias to check if a 2d position is inside a circle 
    
    Args:
        key (str): node key
        xy_nodes (list of :class:`BaseNode`): two nodes returning x and y coordinates 
        x0, y0 (float): circle origin 
        r (float): circle radius
    
    """
        
    def __init__(self, key: str, xy_nodes,  x0 :float = 0.0, y0: float = 0.0, r: float = 0.0): 
        a,b = xy_nodes
        super().__init__(key, xy_nodes)
        self.x0 = x0
        self.y0 = y0 
        self.r2 = r*r 
        
    def fget(self, x, y):
        return ((x-self.x0)**2 + (y-self.y0)**2) < self.r2        
    

class PosNameNode(NodeAlias):
    """ Node alias returning a position name thanks to a list of position and a tolerance 
    
    Args:
        key (str):  node key 
        node (:class:`BaseNode`)
        poses (dict):  name, position pairs
        tol (float): tolerence for each poses
        unknown (str, optional): string for unknown position 
        
    Example:
       
    :: 
       
       PosNameNode('pos_name', motor1.stat.pos_actual, {'FREE':0.0, ''})
    """
    def __init__(self, 
           key: str, 
           node: BaseNode, 
           poses: Dict[str,float] = None, 
           tol: float = 0.0, 
           unknown: str = ""
         ) -> None: 
        super().__init__(key, node)
        self.poses = {} if poses is None else poses
        self.tol = tol
        self.unknown = unknown 
    
    def fget(self, value: float) -> str:
        for name, pos in self.poses.items():
            if abs(pos-value)<self.tol:
                return name
        return self.unknown
        
