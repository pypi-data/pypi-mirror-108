from .base import _BaseObject, _BaseProperty

class BaseManager(_BaseObject):
    def __init__(self, key):
        self._key = key
    
    @property
    def key(self):
        return self._key 
    
    @classmethod
    def prop(this_class, name, *args, **kwargs):
        kwargs.setdefault('cls', this_class)
        return ManagerProperty(name, *args, **kwargs)
    
    def clear(self):
        """ clear all cashed intermediate objects """
        self._clear_all()
    
class ManagerProperty(_BaseProperty):
    _cls = BaseManager # default class 
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
    
    def _finalise(self, parent, device):
        # overwrite the fget, fset function to the node if defined         
        if self.fbuild:
            self.fbuild(parent, device)  
                      
managerproperty = BaseManager.prop
