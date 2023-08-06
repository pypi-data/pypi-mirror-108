import opcua
from opcua import ua
from typing import Optional, Any
from pydevmgr_core.node import BaseReadCollector, BaseWriteCollector

def _ua_server_sid(client):
    """ Used in node to get a unique id per server 
    
    When for instance using download or upload method the coms are grouped 
    by server ID to allow one single call per server. 
    """
    u = client.server_url
    return (u.hostname, u.port) 

######
#  Some special Vars with no or ambigous native python equivalent 

def Int16(value:int) -> ua.Variant:
    return ua.Variant(int(value), ua.VariantType.Int16) 
INT = Int16

def Int32(value: int) -> ua.Variant:
    return ua.Variant(int(value), ua.VariantType.Int32)
DINT = Int32

def Int64(value: int) -> ua.Variant:
    return ua.Variant(int(value), ua.VariantType.Int64)  
LINT = Int64

def UInt16(value: int) -> ua.Variant:
    return ua.Variant(int(value), ua.VariantType.UInt16) 
UINT = UInt16

def UInt32(value: int) -> ua.Variant:
    return ua.Variant(int(value), ua.VariantType.UInt32)
UDINT = UInt32

def UInt64(value: int) -> ua.Variant:
    return ua.Variant(int(value), ua.VariantType.UInt64)        
ULINT = UInt64

def Float(value: float) -> ua.Variant:
    return ua.Variant(float(value), ua.VariantType.Float)
REAL = Float

def Double(value: float) -> ua.Variant:
    return ua.Variant(float(value), ua.VariantType.Double)
LREAL = Double




##
# Read and write collectors for OPC-UA 

class UAReadCollector:
    """ A Collector to read the value of multiple opc-ua nodes in one roundtrip 
    
    Args:
        uaclient (:class:`opcua.Client`)
    """
    def __init__(self, uaclient: opcua.Client) -> None:
        params =  ua.ReadParameters()
        params.uaclient = uaclient
        self._keys = list()
        self._params = params
                
    def add(self, node) -> None:
        """ Add a UaNode to the queue 
        
        Args:
            node (:class:`pydevmgr.UaNode`): node to add in the key. 
                Note this is a pydevmgr UaNode and not an opcua.Node
        """
        rv = ua.ReadValueId()
        rv.NodeId = node.uanodeid
        rv.AttributeId = ua.AttributeIds.Value
        self._params.NodesToRead.append(rv)
        self._keys.append(node.key)
    
    def read(self, data: dict) -> None:
        """ read all data from server and feed result in the input dictionary """
        result = self._params.uaclient.read(self._params)
        for key,r in zip(self._keys, result):
            r.StatusCode.check()
            data[key] =  r.Value.Value 

class UAWriteCollector:
    """ A Collector to write the value of multiple opc-ua nodes in one roundtrip 
    
    Args:
        uaclient (:class:`opcua.Client`)
    """
    def __init__(self, uaclient: opcua.Client) -> None:
        params =  ua.WriteParameters()
        params.NodesToWrite = []        
        params.uaclient = uaclient
        self._params = params
        
        
    def add(self, node, value: Any) -> None:   
        """ Add a node and its attached value to the queue 
        
        Args:
            node (:class:`pydevmgr.UaNode`): node to add in the key. 
                Note this is a pydevmgr UaNode and not an opcua.Node
            value (any): value to be writen 
        
        """ 
        wv = ua.WriteValue()
        wv.NodeId = node.uanodeid
        wv.AttributeId = ua.AttributeIds.Value
        self._params.NodesToWrite.append(wv)
        wv.Value = node._parse_value_for_ua(value)
    
    def write(self) -> None:
        """ Write all values to server """
        params = self._params
        result = params.uaclient.write(params)
        for r in result: 
            r.check()


class UaComNode:
    """ A class interface for opcua.Node 
    
    Function used in the context of pydevmgr are re-defined here. 
    
    This interface could be replaced by a simululator :class:`UaSimComNode` for debugging purposes
    
    Args:
        us_node (:class:`opcua.Node`)
        sid (optional, any): hashable object (most likely str). Defines an unique server id.
    """
    def __init__(self, ua_node: opcua.Node, sid: Optional[Any] = None) -> None:
        self._ua_node = ua_node
        self._sid = sid
        self._ua_variant_type = None
    
    @property
    def sid(self) -> Any:
        """ Unique server identification. shall be any hashable object """        
        if self._sid:
            return self._sid            
        # in case UaComNode has not be created by UaCom , the sid was missing 
        # so we need to create one from the client=server information
        # The only way I found is this one if their is a connection
        if self._ua_node.server._uasocket:
            if self._ua_node.server._uasocket._socket.socket.fileno()>0:
                self._sid = self._ua_node.server._uasocket._socket.socket.getpeername()
                return self._sid
        # unconnected sid, should not really mater what the output is 
        return 999        
    
    @property
    def nodeid(self) -> ua.NodeId:
        return self._ua_node.nodeid
    
    def get_value(self) -> Any:
        """ get the node value from server """
        return  self._ua_node.get_value()
    
    def set_value(self, datavalue: ua.DataValue) -> None:
        """ set the node value to server 
        
        Args:
            data value (:class:`ua.DataValue`): DataValue as returned by the method :meth:`UaComNode.parse_value`
        """
        self._ua_node.set_attribute(ua.AttributeIds.Value, datavalue)
    
    def parse_value(self, value: Any) -> ua.DataValue:
        """ parse a value to a  :class:`ua.DataValue` 
        
        Args:
            value (int, float, str, :class:`ua.Variant`,  :class:`ua.DataValue`)
                note if int, to remove ambiguity between int64, int32, the real variant is asked to 
                the server the first time than cashed. This should rarely append as UA type will be defined 
                in the :class:`pydevmgr.UaNode` definition.
                
        """
        if isinstance(value, (int,)):
            # remove embiguity between int64 and int32, int16
            # we need to ask the variant_type on the server
            if self._ua_variant_type is None:
                self._ua_variant_type = self._ua_node.get_data_type_as_variant_type()
            datavalue = ua.DataValue(ua.Variant(value, self._ua_variant_type))
        elif isinstance(value, ua.DataValue):
            datavalue = value
        elif isinstance(value, ua.Variant):
            datavalue = ua.DataValue(value)
        else:
            datavalue = ua.DataValue(value)
        return datavalue 
                
    def call_method(self, methodid, *args) -> int:
        """ Call a method of the node 
        
        see :meth:`opcua.Node.call_method`    
        """
        return self._ua_node.call_method(methodid, *args)
        
    def read_collector(self) -> UAReadCollector:
        """ Return a :class:`UAReadCollector` to collect nodes for reading node values on the server """
        return UAReadCollector(self._ua_node.server)
        
    def write_collector(self) -> UAWriteCollector:
        """ Return a :class:`UAWriteCollector` to collect nodes for writing node values on the server """
        return UAWriteCollector(self._ua_node.server)


class UaCom:
    """ This is a wrapper arround the :class:`opcua.Client`
    
    All objects,  :class:`pydevmgr.UaDevice`, :class:`pydevmgr.UaInterface`, ... will use 
    an :class:`UaCom` instance to communicate to OPCUA.
    :class:`pydevmgr.UaNode`  and :class:`pydevmgr.UaRpc` will use a :class:`UaComNode` instance.
    
    The idea is that one can replace this object by anything else to cover special needs. 
    E.g. to make a simulator for instance
    The simulator should define the same method as in UaCom and UaComNode 
    
    Args:
        address (optional, str): needed if `ua_client` is None
             server url address as e.g. "opc.tcp://192.168.1.28:4840"
        ua_client (optional, :class:`opcua.Client`): needed if address is None
            is this Client instead of creating one from the address 
    
    """
    def __init__(self, 
          address: Optional[str] = None,
          ua_client: opcua.Client = None
        ):
        if ua_client:
            self._ua_client = ua_client
        elif address:
            self._ua_client = opcua.Client(address)
        else:
            raise ValueError('address and ua_client cannot be both None')
    
    @property
    def sid(self) -> tuple:
        u = self._ua_client.server_url
        return (u.hostname, u.port) 
    
    def connect(self) -> None:
        """ connect client to server """
        self._ua_client.connect()
    
    def disconnect(self) -> None:
        """ disconnect client """
        self._ua_client.disconnect()
    
    def get_node(self, nodeid: str) -> UaComNode:
        """ Return an :class:`UaComNode` according to the string Node Id 
        
        Args:
            nodeid (str)
        """
        return UaComNode(self._ua_client.get_node(nodeid), self.sid)
    
    def read_collector(self) -> UAReadCollector:
        """ Return a :class:`UAReadCollector` to collect nodes for reading node values on the server """
        return UAReadCollector(self._ua_client.uaclient)

    def write_collector(self) -> UAWriteCollector:
        """ Return a :class:`UAWriteCollector` to collect nodes for writing node values on the server """
        return UAWriteCollector(self._ua_client.uaclient)   
    
    def is_connected(self) -> bool:
        """ True if the com is connected to the server """
        if self._ua_client.uaclient and self._ua_client.uaclient._uasocket:
            t = self._ua_client.uaclient._uasocket._thread
            return t and t.is_alive()
        return False
    

# ########## ########## ########## ########## 
#   UACOM Simulator 
#  Protypes not sure we need to use as simulators can be run independantly
   
from dataclasses import dataclass , field
@dataclass
class SimNodeData:
    nodeid: str = ""
    value: Any = None
    methods: dict = field(default_factory=dict)
    
    
class UaSimComNode:
    def __init__(self, simdata: Optional[SimNodeData], sid: Optional[Any] = None) -> None:        
        self._sid = sid 
        self._ua_variant_type = None
        self._sim = SimNodeData() if simdata is None else simdata
        
    @property
    def sid(self) -> str:        
        if self._sid:
            return self._sid            
        # in case UaComNode has not be created by UaCom , the sid was missing 
        # so we need to create one from the client=server information
        # The only way I found is this one if their is a connection
        return id(self)
    
    @property
    def nodeid(self) -> ua.NodeId:
        return self._sim.nodeid
    
    def get_value(self) -> Any:
        return self._sim.value
    
    def set_value(self, datavalue: ua.DataValue) -> None:
        self._sim.value = datavalue
    
    def parse_value(self, value: Any) -> ua.DataValue:
        return value
                
    def call_method(self, methodid, *args) -> int:
        return self._sim.methods[methodid](*args)
        
    def read_collector(self) -> BaseReadCollector:
        return BaseReadCollector()
        
    def write_collector(self) -> BaseWriteCollector:
        return BaseWriteCollector()
        

class UaSimCom:
    """ """
    def __init__(self,           
          simdata: Optional[dict] = None
        ):
        self._sim = {} if simdata is None else simdata
        
    @property
    def sid(self) -> tuple:
        return id(self)
    
    def connect(self) -> None:
        pass
    
    def disconnect(self) -> None:
        pass
    
    def get_node(self, nodeid: str) -> UaComNode:        
        simdata = self._sim.setdefault(nodeid, SimNodeData())        
        return UaSimComNode(simdata, self.sid)
    
    
    def read_collector(self) -> BaseReadCollector:
        return BaseReadCollector()

    def write_collector(self) -> BaseWriteCollector:
        return BaseWriteCollector()   
    
    def is_connected(self) -> bool:
        return True
    




       
