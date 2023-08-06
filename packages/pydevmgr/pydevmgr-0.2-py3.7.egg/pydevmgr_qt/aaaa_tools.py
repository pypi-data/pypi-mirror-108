from pydevmgr import Device, RpcError, GROUP
from typing import List, Union, Tuple, Callable, Optional
from PyQt5.QtWidgets import QComboBox, QWidget


_enum = -1 
def _inc(i=None):
    """ number increment to use in frontend 
    
    _inc(0) # reset increment to 0 and return 0 
    _inc()  # increment and return incremented number 
    """
    global _enum
    _enum = _enum+1 if i is None else i
    return _enum

# TODO: change this by a real logging system 
error = print

class STYLE(GROUP):
    """ A collection of style IDs derived from GROUPs in pydevmgr + extra stuff """
    NORMAL  = "NORMAL"
    ODD     = "ODD"
    EVEN    = "EVEN"
    ERROR_TXT = "ERROR_TXT"
    OK_TXT =    "OK_TXT"
    DIFFERENT = "DIFFERENT"
    SIMILAR = "SMILAR"
    
""" Associate STYLE IDs to qt stylSheet """
qt_style_loockup = {
    STYLE.NORMAL  : "background-color: white;",
    STYLE.IDL     : "background-color: white;",
    STYLE.WARNING : "background-color: #ff9966;",
    STYLE.ERROR   : "background-color: #cc3300;",
    STYLE.OK      : "background-color: #99cc33;",
    STYLE.NOK     : "background-color: #ff9966;",
    STYLE.BUZY    : "background-color: #ffcc00;",
    STYLE.UNKNOWN : "",
    STYLE.ODD     : "background-color: #E0E0E0;",
    STYLE.EVEN    : "background-color: #F8F8F8;",
    STYLE.ERROR_TXT : "color: #cc3300;",
    STYLE.OK_TXT : "color: black;",
    STYLE.DIFFERENT : "color: #cc3300;",
    STYLE.SIMILAR: "color: black;",
}

def get_style(style):
    return qt_style_loockup.get(style, "")

""" Associate a state to a style """
state_style_loockup = {
   Device.STATE.NONE  : STYLE.UNKNOWN, 
   Device.STATE.OP    : STYLE.OK, 
   Device.STATE.NOTOP : STYLE.NOK,
}


class Feedback:
    """ Protect some code inside a with statement 
    
    If feedback function is given, it is called in case of error 
    """
    
    def __init__(self, 
        feedback: Callable[[list,Exception], None], 
        catched: tuple = (Exception,)
        ):
        if feedback is None:
            def feedback(messages, er):
                if er: 
                    raise er
        
        self.feedback = feedback
        self.messages = []
        self.catched = catched 
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, exc_traceback):         
        if exc_value is None:
            self.feedback(None, "")
        else:
            if issubclass( exc_type, self.catched):
                self.feedback(exc_value, str(exc_value))
                #self.feedback(self.messages, exc_value)
                return True
            else:
                raise exc_value 
            
    def add_msg(self, msg):
        self.messages.append(str(msg))        




class Action:
    def __init__(self, parent, func, inputs=None, feedback=None, before=None, after=None):        
        inputs = [] if inputs is None else inputs        
        # transform contant to lambdas function
        clean_inputs = []
        
        self._disconnection = parent._disconnection
        self._combos = parent._combos
                        
        for input in inputs:
            if not hasattr(input, "__call__"):
                input = lambda __cte__ = input: __cte__
            clean_inputs.append(input)
                        
        fdbk =  Feedback(feedback, (RpcError,TypeError,ValueError,RuntimeError))
        
        if feedback is None:
            pass
        else:         
            def func_call():            
                try:
                    if before: before()   
                    func(*(fi() for fi in clean_inputs))
                    if after: after()
                except (RpcError,TypeError,ValueError,RuntimeError) as er:
                    return feedback(er, str(er))
                    
        self.run = func_call
            
    def run(self):
        raise NotImplementedError('run')    
    
    def connect_button(self,        
        button: QWidget
      ) -> None:      
        button.clicked.connect(self.run)
        self._disconnection.append( button.clicked.disconnect )
    
    def connect_checkbox(self, 
        checkbox
    ) -> None:
        checkbox.stateChanged.connect(self.run)
        self._disconnection.append( checkbox.stateChanged.disconnect ) 
        
    def connect_item(self,         
        combo: QComboBox, 
        item_id: int        
     ) -> None:
        try:
            f, item2action = self._combos[combo]
        except KeyError:
            self._new_combo(combo)
            f, item2action = self._combos[combo]        
        item2action[item_id] = self
        
    def _new_combo(self, combo):
        if combo in self._combos:
            try:
                combo.currentIndexChanged.disconnect()
            except TypeError:
                pass
                        
        item2action = {}
        def combo_call(i):
            try:
                action = item2action[i]
            except KeyError:
                return 
            action.run()            
        
        self._combos[combo] = (combo_call, item2action)
        combo.currentIndexChanged.connect(combo_call)
        self._disconnection.append(combo.currentIndexChanged.disconnect)
    
        
    
        
    
        
        
class Actions2:
    def __init__(self):        
        self._disconnection = []
        self._combos = {}
        
    def add(self, func, inputs=None, feedback=None, before=None, after=None):
        return Action(self, func, inputs, feedback=feedback, before=before, after=after)
        
    def disconnect(self):
        for f in self._disconnection:
            try:
                f()
            except TypeError:
                pass
    
        
        
class Actions:
    def __init__(self, config: List[Union[str, Tuple[str, Optional[Callable], list]]]):
        self.config = config
        self._disconnection = []
        
    def connect_combo(self,
        combo: QComboBox, 
        feedback: Optional[Callable] = None, 
        reset: Optional[Callable] = None
      ) -> Callable:
        self.setup_combo(combo)
        f = self.combo_func(feedback=feedback, reset=reset)
        combo.currentIndexChanged.connect(f)
        self._disconnection.append( combo.currentIndexChanged.disconnect )
        return f
    
    def connect_button(self, 
        idx: int, 
        button: QWidget, 
        feedback: Optional[Callable] = None, 
        reset: Optional[Callable] = None
      ) -> Callable: 
        item = self.config[idx]
        if isinstance(item, str):
            return 
        name, func, _ = item
        if func is None: return     
        
        f = self.button_func(idx, button, feedback=feedback, reset=reset)
        button.clicked.connect(f)
        self._disconnection.append(button.clicked.disconnect)
        return f
    
            
    def setup_combo(self, combo: QComboBox):        
        idx = combo.count()
        for item in self.config:
            if isinstance(item, str):
                if item == "---":
                    combo.insertSeparator(idx)
                    # inserting a separator increase the index so add a dummy action    
                else:
                    name = item
                    item = (name, None, [])
                    combo.addItem(name)
                    
            else:
                name, _, _ = item
                combo.addItem(name)
            idx = combo.count()
    
    def combo_one_func(self,
        feedback: Optional[Callable] = None, 
        reset: Optional[Callable] = None
    ) -> Callable:
        fdbk =  Feedback(feedback, (RpcError,TypeError,ValueError,RuntimeError))
        
    
    def combo_func(self, 
           feedback: Optional[Callable] = None, 
           reset: Optional[Callable] = None
        ) -> Callable:
                
        fdbk =  Feedback(feedback, (RpcError,TypeError,ValueError,RuntimeError)) 
               
        def call_method(idx):
            with fdbk as f:
                item = self.config[idx]
                if isinstance(item, str):
                    return 
                else:                    
                    _, func, input_funcs = item 
                
                if func is None:
                    return 
                
                func(*(fi() for fi in input_funcs))
                if reset: reset()      
        return call_method                           

    def button_func(self, 
        idx: int, 
        button: QWidget, 
        feedback: Optional[Callable] = None, 
        reset: Optional[Callable] = None
        ) -> Callable:
        
        fdbk =  Feedback(feedback, (RpcError,TypeError,ValueError,RuntimeError)) 
        
        def call_method():
            with fdbk as f:
                item = self.config[idx]
                if isinstance(item, str):
                    return 
                else:                    
                    _, func, input_funcs = item 
                
                if func is None:
                    return                                 
                func(*(fi() for fi in input_funcs))                
                if reset: reset()   
        return call_method           
    
    def disconnect(self):
        for f in self._disconnection:
            try:
                f()
            except TypeError:
                pass    
                
            
def method_setup(combo, items):
    """ Does the same thing than combo_box.setItems 
    
    except that input is a list of (name, func, input_func) as for  method_switcher
    
    Args:
       combo: A QT Combo widget 
       items (iterable):  A list of string or tuple 
            If tuple, this shall be (name, func, list_of_inputs) where:
                - `name` is the displayed name 
                - `func` is a callable function which take `len(list_of_inputs)` arguments
                - `list_of_inputs` is a list of callable which returns the arguments 
            If str:
               - if "---" this is set as separator 
               - otherwise add the item without callback function 
    
    Returns:
        items: A copy of input items cleaned from string and separators 
               items ready to be used by :func:`method_switcher`
               
    ..seealso::
       method_switcher
    """
    output= []
    idx = combo.count()
    for item in items:
        if isinstance(item, str):
            if item == "---":
                combo.insertSeparator(idx)
                # inserting a separator increase the index so add a dummy action
                output.append(("", None, []))
                
            else:
                name = item
                item = (name, None, [])
                combo.addItem(name)
                output.append(item)
        else:
            name, _, _ = item
            combo.addItem(name)
            output.append(item)
        idx = combo.count()
    return output 

def method_caller(func, input_funcs, feedback=None):
    """ Build a method to togle a function 
    
    Args:
        func (callable): function to call
        input_funcs (list of callable): each member return an argument for the function
        feedback: func with signature func(er, txt)
    
    Returns:
        method : a callable obect with signature func()
        
    """
    if feedback:        
        def call_method():
                      
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError) as e:
                feedback(True, str(e))
            else:
                feedback(False, '')
    else:
        def call_method():
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError) as e:
                error(str(e))    
    return  call_method
    
def method_switcher( func_inputs, feedback=None, reset=None):
    """ Build method that take an index number and trigger the associated method 
    
    
    Args:
        func_inputs (iterable):  A list of  tuple 
            Shall be (name, func, list_of_inputs) where:
                 - `name` is the displayed name 
                 - `func` is a callable function which take `len(list_of_inputs)` arguments
                    The function will be triggered when the item is selected 
                 - `list_of_inputs` is a list of callable which returns the arguments for func
        feedbac: (optional, callable): func with signature func(er,txt)
            if success  feedback(False,'') is returned 
            if failure  feedback(True, error) is returned
            
            When feedback is None, the error is just printed on STDOUT 
        reset (optional, callable): to execute after each method call
    
    Returns:
        method : a callable obect with signature func(i) ready to be connected to a combo widget 
                 e.g.: combo.currentIndexChanged.connect(method_switcher(...)) 
        
    """
    if feedback:    
        def call_method(idx):
            _, func, input_funcs = func_inputs[idx]
            if func is None:
                return 
            
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError,RuntimeError) as e:
                feedback(True, e)
            else:
                feedback(False, '')
            if reset: reset()
    else:
        def call_method(idx):
            _, func, input_funcs = func_inputs[idx]
            if func is None:
                return 
            try:
                func(*(fi() for fi in input_funcs))
            except (RpcError,TypeError,ValueError,RuntimeError) as e:
                error(str(e))
            if reset: reset()
    
    return call_method                           


_pydevmgr_widgets = {}
def record_widget(widget_type, dev_type, constructor):
    """ Record a new widget class constructor 
    
    Args:
        widget_type (string): description of the widget like "ctrl"
        dev_type (:class:`Device`): A device class 
        constructor (callable): A constructor for the widget  
    """
    _pydevmgr_widgets[(widget_type, dev_type)] = constructor

def get_widget_constructor(widget_type, dev_type):
    """ Return a Widget class constructor 
    
    Args:
    
        widget_type (str): 
                      - 'line' a one line widget for the device 
                      - 'ctrl' a complete control but still compact widget 
        dev_type (str): device type (e.g. "Motor", "Adc", ...)
    
    The widget constructor must have been recorded by the :func:`record_widget` function
    """
    try:
        return _pydevmgr_widgets[(widget_type, dev_type)]
    except KeyError:
        raise ValueError("Unknown widget of type {} for a {}".format(widget_type, dev_type))

