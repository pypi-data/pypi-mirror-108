from typing import Iterable , Any
from inspect import signature 

_parse_loockup = {}
def record_parse_func(name, func):
    global _parse_loockup
    _parse_loockup[name] = func

def get_parse_func(name):
    try:
        return _parse_loockup[name] 
    except KeyError:
        raise ValueError(f"Unknown parser function {name}")

def _defaults(obj):
    def default_setter(f):
        setattr(obj, "set_default_parameters", f)
        return obj
    return default_setter

def _record(name, *args):
    def recorder(f):
        record_parse_func(name, f)
        for n in args:
            record_parse_func(n, f)
        return f
    return recorder

def _npos_params(f):
    try:
        parameters = signature(f).parameters
    except ValueError:
        # some builtin type like int, bool has no signature so a ValueError is raised 
        return 0 
    np = 0
    for p in parameters.values():
        if p.kind == p.POSITIONAL_OR_KEYWORD and p.default is p.empty:
            np += 1
        else:
            break    
    return np

class ParserParameters(dict):
    def __getattr__(self, attr):
        try:
            return self.__getitem__(attr)
        except KeyError:
            raise AttributeError(attr)
    
    def __setattr__(self, attr, value):
        self.__setitem__(attr, value)
    
        
            
class Parser:
    """ A Value Parser object 
    
    The parser is a callable object it is made from a list of callable with the signature f(v,d) 
    where v is the value to parse and d is a dictionary containing the necessary properties for
    parsing the value
    
    for instance ``clipped`` will look at d['min'] and d['max'] property
    The dictionary of property is the same for all function on the list
    
    Example:
       
       ::
        
        >>> from pydevmgr_core.parser import *  
        >>> p = Parser( [tofloat, clipped], min=0.0, max=100.0 )
        >>> p = Parser( ['tofloat', 'clipped'], min=0.0, max=100.0 )  # fnuc are also known by string 
        >>> p(4.5)
        4.5
        >>> p('4.5')
        4.5
        >>> p(123)
        100.0
      
        >>> p = Parser( [lowered, loockup] , loockup=["a", "b", "c"])
        >>> p('A')
        'a'
        >>> p('z')
        ValueError: must be one of ['a', 'b', 'c'] got z
        
        >>> p = Parser( [lowered, loockup] , loockup=["a", "b", "c"], loockup_default="???")
        >>> p('z')
        '???'
        
    """
    _parameters = None
    _funcs = None
    def __init__(self, parse_list: Iterable, **parameters):
        
                
        flist = []
        for f in parse_list:
            if isinstance(f, str):
                f = get_parse_func(f)
                
            # elif isinstance(f, Parser):
            #     for k,v in f._parameters.items():
            #         parameters.setdefault(k,v)
            #     flist.extend(f._funcs)
            elif hasattr(f, "__call__"):
                pass
            else:
                raise ValueError("parsers must be a callable or a string got a {}".format(type(f)))            
            flist.append((f, _npos_params(f)>1))
            if hasattr(f, "set_default_parameters"):
                f.set_default_parameters(parameters)    
            
        self.__dict__['_parameters'] = ParserParameters(parameters)
        self.__dict__['_funcs'] = flist
    
    def __call__(self, value):
        p = self._parameters
        for f,np in self._funcs:
            if np:
                value = f(value, p)
            else:
                value = f(value)
        return value
    
    @property
    def parameters(self):
        return self._parameters
        
    def __repr__(self):
        p = ", ".join("%s=%r"%(k,v) for k,v in self._parameters.items())
        return "<%s %s>"%(self.__class__.__name__, p)
            
# ##########################################
@_record('clipped')
def clipped(value: float, p: dict):
    min = p.get('min', None)
    max = p.get('max', None)
    if min is not None and value<min :
        return min
    if max is not None and value>max :
        return max
    return value
    
@_defaults(clipped)
def clipped(p):
    p.setdefault('min', None)
    p.setdefault('max', None)

# ##########################################        
@_record('bounded')
def bounded(value: float, p: dict):
    min = p.get('min', None)
    max = p.get('max', None)
    if min is not None and value<min :
        raise ValueError(f'{value} is lower than {min}')
    if max is not None and value>max :
        raise ValueError(f'{value} is higher than {max}')
    return value
     
@_defaults(bounded)
def bounded(p):
    p.setdefault('min', None)
    p.setdefault('max', None)
# ##########################################

@_record('loockup')
def loockup(value: Any, p: dict):
    loockup = p.get('loockup', [])
    if value not in loockup:
        try:
            return p['loockup_default']
        except KeyError:            
            raise ValueError(f'must be one of {loockup} got {value}')
    return value
    
@_defaults(loockup)
def loockup(p):
    p.setdefault('loockup', [])

# ##########################################

@_record('rounded')
def rounded(value: float, p: dict):
    ndigits = p.get('ndigits', None)
    return round(value, ndigits)  

@_defaults(rounded)
def rounded(p):
    p.setdefault('ndigits', None)






# ##########################################

@_record('tostring', 'string')
def tostring(value: Any, p: dict):
    fmt = p.get('format', '%s')
    return fmt%(value,)
@_defaults(tostring)
def tostring(p):
    p.setdefault('format', '%s')
  
# ##########################################

@_record('capitalized')
def capitalized(value: str, p: dict):
    return value.capitalize()

# ##########################################
@_record('lowered', 'lower')
def lowered(value: str, p: dict):
    return value.lower()
# ##########################################
@_record('uppered', 'upper')
def uppered(value: str, p: dict):
    return value.upper()

# ##########################################
@_record('stripped')
def stripped(value: str, p: dict):
    return value.strip(p.get('strip',None))
    

@_defaults(stripped)
def stripped(p):
    p.setdefault('strip', None)

# ##########################################    
@_record('lstripped')
def lstripped(value: str, p: dict):
    return value.lstrip(p.get('lstrip',None))
    

@_defaults(lstripped)
def lstripped(p):
    p.setdefault('lstrip', None)

# ##########################################    

_record('rstripped')
def rstripped(value: str, p: dict):
    return value.rstrip(p.get('rstrip',None))
    

@_defaults(rstripped)
def rstripped(p):
    p.setdefault('rstrip', None)

# ##########################################    
