from typing import Any,  Tuple

def kjoin(*args) -> str:
    """ join key elements """
    return ".".join(a for a in args if a)

def ksplit(key: str) -> Tuple[str,str]:
    """ ksplit(key) ->  prefix, name
    
    >>> ksplit('a.b.c')
    ('a.b', 'c')
    """
    s, _, p = key[::-1].partition(".")
    return p[::-1], s[::-1]

def join_key(parent: Any, name: str) -> str:
    """ Join parent key and a name 
    
    If parent has `.join_key` method parent.join_key(name) is returned
    Otherwhise kjoin(parent.key, name) is returned.    
    """
    try:
        jk = parent.join_key
    except AttributeError:
        try:
            key = parent.key
        except AttributeError:
            raise ValueError("parent object must have `join_key` method or `key` attribute")
        return kjoin(key, name)
    else:
        return jk(name)


def split_key(obj) -> Tuple:
    """ Split the object key in (prefix, name) tuple 
    
    if object has the .split_key method it is called and result returned 
    otherwhise ksplit(obj.key) is returned 
    """
    try:
        sk = obj.split_key
    except AttributeError:
        try:
            key = obj.key
        except AttributeError:
            raise ValueError("object must have `split_key` method or `key` attribute")
        return ksplit(key)
    else:
        return sk()
        

class _BaseObject:
    __all_cashed__ = False
    def __init__(self, key):
        # init must be redefined, the only requirement is to have the 'key' argument as first positional argument 
        self._key = key 
    
    def __repr__(self):
        return "<{} key={!r}>".format(self.__class__.__name__, self._key)
    
    def join_key(self, *names):        
        names = (self._key,)+names
        return ".".join(a for a in names if a)
    
    def split_key(self):
        s, _, p = self._key[::-1].partition(".")
        return p[::-1], s[::-1]
    
    @classmethod
    def new(cls, parent, name):
        """ a base constructor for BaseNode 
        
        parent must have the .join_key method
        """
        # This will be redefined function to the parent context
        return cls( parent.join_key(name) )
    
    @classmethod
    def prop(cls, name):
        # redefined in the object declaration
        return _BaseProperty(name, cls=cls)
    
    @property
    def key(self):
        """ node key """
        return self._key
        
    @property
    def name(self):
        return ksplit(self._key)[1]    
    
    def _cash_all(self):
        """ cash all child _BaseProperty to real Objects """
        if not self.__all_cashed__:
            for sub in self.__class__.__mro__:
                for k,v in sub.__dict__.items():
                    if isinstance(v, (_BaseProperty)):
                        getattr(self, k)
            self.__all_cashed__ = True
    
    def _clear_all(self):
        """ clear all cashed intermediate objects """
        for k,v in list(self.__dict__.items()):
            if isinstance(v, (_BaseObject)):
                self.__dict__.pop(k)
        self.__all_cashed__ = False
    

class _BaseProperty:
    
    _cls = None  # must be defined by sub class
    _constructor = None # optional constructor can be defined instead of using the cls.new method
    
    def __init__(self, name,  *args,  **kwargs):
        self._name = name 
        self._pid = name # the object will be stored with this id in parent.__dict__ 
        self._cls = kwargs.pop('cls', self._cls)
        self._constructor = kwargs.pop('constructor',self._constructor)
        
        self._args = args
        self._kwargs = kwargs
    
    def _get_cls_constructor(self, parent):
        if isinstance(self._cls, str):
            cls = getattr(parent, self._cls)
        else:
            cls = self._cls
        if isinstance(self._constructor, str):
            constructor = getattr(parent, self._constructor)
        else:
            constructor = self._constructor
        return cls, constructor
    
    def _finalise(self, parent, obj):
        pass
    
    def __get__(self, parent, clp=None):
        if parent is None:
            return self 
        # try to retrieve the node directly from the parent __dict__ where it should 
        # be cached. If no boj cached create one and save it/ 
        # if _pid is the same than the attribute name in class, this should be called only ones        
        try:
            obj = parent.__dict__[self._pid]
        except KeyError:
            cls, constructor = self._get_cls_constructor(parent)            
            if constructor is None:
                obj = cls.new(parent, self._name, *self._args, **self._kwargs)
            else:
                obj = constructor(cls, self._name, *self._args, **self._kwargs)            
            self._finalise(parent, obj)            
            parent.__dict__[self._pid] = obj        
        return obj
        
    def new(self, parent):
        cls, constructor = self._get_cls_constructor(parent)            
        if constructor is None:
            obj = cls.new(parent, self._name, *self._args, **self._kwargs)
        else:
            obj = constructor(cls, self._name, *self._args, **self._kwargs)            
        self._finalise(parent, obj)
        return obj                
        