from pydantic import BaseModel
from pydevmgr import NodeVar, DataLink, UaDevice, Downloader
from .tools import STYLE, Feedback, method_switcher, record_widget, method_setup, get_style, get_widget_constructor
from PyQt5 import uic
from PyQt5.QtWidgets import QFrame, QCheckBox
from .base import BaseUi
from .widget_io import gattr, sattr, gsattr, BoolKeyVal_IO, FloatKeyVal_IO, IntKeyVal_IO, EnumKeyVal_IO
from .io import find_ui

from .base_ctrl import BaseStatData, BaseData, BaseModel
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum 
        
def float_nan(t):
    try:
        return float(t)
    except (ValueError, TypeError):
        return None

def int_nan(t):
    try:
        return int(t)
    except (ValueError, TypeError):
        return None    

def b2t(b):
    return "[X]" if b else "[_]"

def switch_style(w,b):
    style = STYLE.SIMILAR if b else STYLE.DIFFERENT
    w.setStyleSheet(get_style(style))


def _dummy(data):
    pass

def _bool_txt(output, key):
    def update_output(data):
        b = getattr(data, key)
        t = b2t(b)
        

class BaseKey:
    def __init__(self, update_input, update_output, update_data):
        self.update_input = update_input
        self.update_output = update_output
        self.update_data = update_data
    
    def disconnect(self):
        self.update_input =  _dummy
        self.update_output = _dummy
        self.update_data =   _dummy
        
            
class BoolKey(BaseKey):
    
    def __init__(self, key, input, output, feedback=None, default=False):
            
        if isinstance(input, QCheckBox) and hasattr(output, "setText"):
            def update_input(data):
                b = getattr(data, key)
                input.setChecked(b)
            def update_output(data):
                b = getattr(data, key)
                t = b2t(b)                
                output.setText(t)
                switch_style(output, input.isChecked()==b)
            def update_data(data):
                setattr(data, key, input.isChecked())
        else:
            raise ValueError("expecting a QCheckBox as input and QLabel as output got %s, %s"%(type(input), type(output)))    
        super().__init__(update_input,update_output,update_data)            
        input.setChecked(default)
        
class FloatKey(BaseKey):
    def __init__(self, key, input, output, feedback=None, fmt="%.3f", default=0.0):
        feedback = Feedback(feedback, (ValueError,TypeError))
        if hasattr(input, "setText") and hasattr(output, "setText"):
            def update_input(data):
                v = getattr(data, key)                
                input.setText(fmt%v)
            def update_output(data):
                v = getattr(data, key)
                t = fmt%v                
                output.setText(t)
                switch_style(output, float_nan(input.text())==v)
            def update_data(data):
                with feedback:
                    v = float(input.text())
                    setattr(data, key, v)
        else:
            raise ValueError("Invalid input output combination")    
        super().__init__(update_input,update_output,update_data)    
        if default is not None:
            input.setText(fmt%default)

class IntKey(BaseKey):
    def __init__(self, key, input, output, feedback=None, fmt="%d", default=0):
        feedback = Feedback(feedback, (ValueError,TypeError))
        if hasattr(input, "setText") and hasattr(output, "setText"):
            def update_input(data):
                v = getattr(data, key)                
                input.setText(fmt%v)
            def update_output(data):
                v = getattr(data, key)
                t = fmt%v                
                output.setText(t)
                switch_style(output, int_nan(input.text())==v)
            def update_data(data):
                with feedback:
                    v = int(input.text())
                    setattr(data, key, v)
        else:
            raise ValueError("Invalid input output combination")    
        super().__init__(update_input,update_output,update_data)    
        if default is not None:
            input.setText(fmt%default)
        
class EnumKey(BaseKey):
    
    def __init__(self, key, enum, input, output, feedback=None, fmt="%s: %s", default=None):
        feedback = Feedback(feedback, (ValueError,TypeError))
        num_to_index = {e.value:i for i,e in enumerate(enum)}
        index_to_num = {i:e.value for i,e in enumerate(enum)}
        if hasattr(input, "setCurrentIndex") and hasattr(output, "setText"):
            def update_input(data):
                v = getattr(data, key)                
                input.setCurrentIndex( num_to_index[v] )
                
            def update_output(data):
                a =  enum(getattr(data, key))                                
                output.setText(f"{a.value}: {a.name}")                
                switch_style(output, input.currentIndex()==num_to_index[a.value])
                
            def update_data(data):
                i = input.currentIndex()                
                setattr(data, key, index_to_num[i])
        else:
            raise ValueError("Invalid input output combination")    
        super().__init__(update_input,update_output,update_data)  
        input.clear()
        input.addItems( [a.name for a in enum] )
        if default is not None:
            input.setCurrentIndex( num_to_index[default] )    
            
# place holder for some base setup for config pannels 
# not sure we have any             
class BaseCfg(QFrame, BaseUi):
    keys = None
    def __init__(self, *args, **kwargs):
        self.keys = []  
        super().__init__(*args, **kwargs)                
        
    def add_bool_key(self, key, input_name=None, output_name=None, feedback=None):
        input_name = "in_"+key if input_name is None else input_name
        output_name = key if output_name is None else output_name
        
        self.keys.append(BoolKeyVal_IO(*gsattr(key), 
            getattr(self, input_name), 
            getattr(self,output_name), 
            feedback=feedback)            
            )
        
    def add_float_key(self, key, input_name=None, output_name=None, feedback=None, fmt="%.3f", default=0.0):
        input_name = "in_"+key if input_name is None else input_name
        output_name = key if output_name is None else output_name
        self.keys.append(FloatKeyVal_IO( *gsattr(key), 
                            getattr(self, input_name), 
                            getattr(self, output_name), 
                            fmt=fmt, default=default, feedback=feedback)
                        )
        
    def add_int_key(self, key, input_name=None, output_name=None, feedback=None, fmt="%d", default=0):
        input_name = "in_"+key if input_name is None else input_name
        output_name = key if output_name is None else output_name
        self.keys.append(IntKeyVal_IO( *gsattr(key), 
                            getattr(self, input_name), 
                            getattr(self, output_name), 
                            fmt=fmt, default=default, feedback=feedback)
                        )
    
    def add_enum_key(self, key, enum, input_name=None, output_name=None, feedback=None, default=None):
        input_name = "in_"+key if input_name is None else input_name
        output_name = key if output_name is None else output_name
        self.keys.append(EnumKeyVal_IO( *gsattr(key), enum,
                            getattr(self, input_name), 
                            getattr(self, output_name), 
                            default=default, feedback=feedback)
                        )
            
    def update_outputs(self, data):
        for key in self.keys:
            key.update_output(self, data)
    
    def update_inputs(self, data):
        for key in self.keys:
            key.update_input(self, data)
    
    def update_data(self, data):
        for key in self.keys:
            key.update_data(self, data)
            
    
        
record_widget("cfg", "Device", BaseCfg) 
