import yaml
import os

from pydantic import BaseModel
from typing import Tuple, Optional, List, Dict, Optional, Callable

class IOConfig(BaseModel):
    cfgpath : str = 'CFGPATH'
    yaml_ext : Optional[List[str]] = ('.yml', '.yaml')

ioconfig = IOConfig()
    

def load_config(file_name: str, ioconfig: IOConfig =ioconfig) -> Dict:
    """ Load a configuration 
    
    The file name is given, it should be inside one of the path defined by the $CFGPATH 
    environment variable. 
    
    Args:
        file_name (str): config file name. Should be inside one of the path defined by the $CFGPATH 
        environment variable. Alternatively the file_name can be an abosolute path
        ioconfig (optional): a :class:`IOConfig`        
    """
    return read_config(find_config(file_name, ioconfig=ioconfig))

def read_config(file: str, ioconfig: IOConfig =ioconfig) -> Dict:    
    """ Read the given configuration (yaml) file 
    
    Args:
        file (str): file path, shall be a yaml file. 
    """
    with open(file) as f:
        return yaml.load(f.read(), Loader=yaml.CLoader)

def find_config(file_name, ioconfig: IOConfig =ioconfig):
    """ find a config file and return its absolute path 
    
    Args:
        file_name (str): config file name. Should be inside one of the path defined by the $CFGPATH 
        environment variable. Alternatively the file_name can be an abosolute path
        ioconfig (optional): a :class:`IOConfig`        
    """
    path_list = os.environ.get(ioconfig.cfgpath, '.').split(':')
    for directory in path_list[::-1]:
        path = os.path.join(directory, file_name)
        if os.path.exists(path):
            return  path
    raise ValueError('coud not find config file %r in any of %s'%(file_name, path_list))

    
def explore_config(filter: Optional[Callable] =None, ioconfig: IOConfig = ioconfig):
    """ Iterator on all config files found inside directories of the $CFGPATH environment variable 
    
    Args:
        filter (None, callable, optional): if given it will receive the cfg as red from each file
               to filter
        config (optional): a :class:`IOConfig`               
    """
        
    path_list = os.environ.get(ioconfig.cfgpath, '.').split(':')
    found = set()
    
    for root in path_list[::-1]:
        for r, d, files in os.walk(root):
            for file in files:
                body, ext = os.path.splitext(file)
                if ext in ioconfig.yaml_ext:
                    p = os.path.relpath( os.path.join(r,file), root )
                    if not p in found:
                        if filter:
                            if filter(read_config(os.path.join(r,file))):
                                yield  p, root
                        else:
                            yield  p, root                                    
                    found.add(p)
