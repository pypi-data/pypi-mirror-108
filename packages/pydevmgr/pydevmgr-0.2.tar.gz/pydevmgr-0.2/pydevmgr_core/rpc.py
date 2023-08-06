from .base import _BaseObject, _BaseProperty, ksplit, kjoin
import weakref



class BaseCallCollector:
    """ The Read Collector shall collect all nodes having the same sid and read them in one call
    
    - __init__ : should not take any argument 
    - add : take one argument, the Node. Should add node in the read queue 
    - read : takes a dictionary as arguement, read the nodes and feed the data according to node keys 
    
    The BaseReadCollector is just a dummy implementation where nodes are red one after the other     
    """
    def __init__(self):
        self._rpcs = []
    
    def add(self, rpc, args, kwargs):
        self._rpcs.append((rpc, args, kwargs))
        
    def call(self):        
        for rpc, args, kwargs in self._rpcs:
            rpc.rcall(*args, **kwargs)
                
class RpcError(RuntimeError):
    """ Raised when an rpc method is returning somethingelse than 0

        See rcall method of RpcNode
    """
    rpc_error = 0

class BaseRpc(_BaseObject):
    def __init__(self, key, args_parser=None, kwargs_parser=None):
        super().__init__(key)
        self._args_parser = args_parser
        self._kwargs_parser = kwargs_parser
    
    @classmethod
    def prop(this_cls, name, *args, **kwargs):
        kwargs.setdefault('cls', this_cls)
        return RpcProperty(name, *args, **kwargs)
    
    @property
    def sid(self):
        """ default id server is 0 
        
        The sid property shall be adujsted is the CallCollector
        """
        return 0
        
    def get_error_txt(self, rpc_error):
        """ Return Error text from an rpc_error code """
        return "Not Registered Error"
    
    def call_collector(self):
        """ Return a collector for method call """
        return BaseCallCollector()
    
    def parse_args(self, args, kwargs):
        """ Modify in place a list of args and kwargs thans to the defined args_parser and kwargs_parser """
        if self._args_parser:
            for i,(p,a) in enumerate(zip(self._args_parser, args)):
                args[i] = p(a) 
        if self._kwargs_parser:
            for k,a in kwargs.items():
                try:
                    p = self._kwargs_parser[k]
                except KeyError:
                    pass
                else:
                    kwargs[k] = p(a)
                
    def call(self, *args, **kwargs):
        """ Call the method and return what return the server 
        
        this will mostly return an integer which shall be 0 if success
        
        .. seealso::
        
           :func:`BaseRpc.rcall` method
          
        """
        args = list(args)
        self.parse_args(args, kwargs)
        return self.fcall(*args, **kwargs)
    
    def rcall(self, *args, **kwargs):
        """ Call the Rpc Method but raised an exception in case of an error code is returned """
        e = self.get_error(self.call(*args, **kwargs))
        if e:
            raise e
    
    def get_error(self, rpc_return):
        if rpc_return:
            e = RpcError("RPC ({}): {}".format(rpc_return, self.get_error_txt(rpc_return)))
            e.rpc_error = rpc_return
            return e
    
    def fcall(self, *args, **kwargs):
        raise NotImplementedError('fcall')
    


    
class RpcProperty(_BaseProperty):
    _cls = "Rpc"
    _constructor = None
    fcall = None
    
    def caller(self, func):
        """ decoraotr to define the fcall function """
        self.fcall = func
        return self # must return self
    
    def _finalise(self, parent, rpc):
        if self.fcall:
            parent_wr = weakref.ref(parent)
            def fcall(*args, **kwargs):
                return self.fcall(parent_wr(), *args, **kwargs)
            rpc.fcall = fcall
    
    def __call__(self, func):
        """ The call is used has fcall decorator """
        self.fcall = func
        return self



def rpcproperty(name, *args, **kwargs):
    """ A decorator for a quick rpc creation 
    
    This shall be implemented in a parent interface or any class 
    
    Args:
        cls (class, optional): default is :class:`BaseNode` used to build the node  
        **kwargs: All other arguments necessary for the node construction
    """
    return BaseRpc.prop(name, *args, **kwargs)
    
        
