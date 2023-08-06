from .base import _BaseObject, _BaseProperty, ksplit, kjoin

#  ___ _   _ _____ _____ ____  _____ _    ____ _____ 
# |_ _| \ | |_   _| ____|  _ \|  ___/ \  / ___| ____|
#  | ||  \| | | | |  _| | |_) | |_ / _ \| |   |  _|  
#  | || |\  | | | | |___|  _ <|  _/ ___ \ |___| |___ 
# |___|_| \_| |_| |_____|_| \_\_|/_/   \_\____|_____|
# 

def annotation2node(cls, PropertyClass, arg=None):
    if isinstance(PropertyClass, str):
        PropertyClass = getattr(cls, PropertyClass).prop
    
    if arg is None:
        def mk_kwargs(p):
            return p
        def ckeck(p):
            return isinstance (p, dict)
                                
    elif isinstance(arg, str):
        def mk_kwargs(p):
            if isinstance (p, dict):
                return p
            return {arg:p}
        def check(p):
            return True
        
    else:
        def mk_kwargs(plist):
            if isinstance (plist, dict):
                return plist
            return {k:p for k,p in zip(arg, plist)}
        def check(p):
            return True
        
    for a,p in cls.__annotations__.items():        
        if check(p):
            kwargs = mk_kwargs(p)
            setattr(cls, a, PropertyClass(a, **kwargs))    

def buildproperty(PropertyClass, arg):
    def builder(cls):
        annotation2node(cls, PropertyClass, arg)
        return cls
    return builder 
    


class BaseInterface(_BaseObject):
    """ BaseInterface is holding a key, and is in charge of building nodes """
    
    __all_cashed__ = False
    
    @classmethod
    def prop(this_class, name, *args, **kwargs):
        kwargs.setdefault('cls', this_class)
        return InterfaceProperty(name, *args, **kwargs)
            
    def clear(self):
        """ clear all cashed intermediate objects """
        self._clear_all()        
    
class InterfaceProperty(_BaseProperty):
    _cls = BaseInterface # default class 
    _constructor = None
    fbuild = None
    def builder(self, func):
        """ Decorator for the interface builder """
        self.fbuild = func
        return self
    
    def __call__(self, func):
        """ The call is used has fget decorator """
        self.fbuild = func
        return self
    
    def _finalise(self, parent, interface):
        # overwrite the fget, fset function to the node if defined         
        if self.fbuild:
            self.fbuild(parent, interface)            

interfaceproperty = BaseInterface.prop
    