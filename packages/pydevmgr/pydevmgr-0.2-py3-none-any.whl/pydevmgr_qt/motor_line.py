from PyQt5 import uic
from PyQt5.QtWidgets import QFrame
from .io import find_ui
from pydevmgr_elt import NodeVar
from .device_line import DeviceLineUi, DeviceLine
from .base import record_widget_factory


class MotorLineStatData(DeviceLine.Data.StatData):
    # DeviceStatData contain state, substate, error code and txt information 
    # Add here all NodeVar needed for the motor GUI    
    pos_actual: NodeVar[float] = 0.0
    pos_name: NodeVar[str]     = ""

class MotorLineData(DeviceLine.Data):
    StatData = MotorLineStatData
    stat: StatData = StatData()


class MotorLineUi(DeviceLineUi):
    def init_ui(self):
        uic.loadUi(find_ui('motor_line_frame.ui'), self)      

class MotorLine(DeviceLine):
    # define the data model (data constructor) for stat     
    Data = MotorLineData
    Widget = MotorLineUi
    
    def init_vars(self):
        super().init_vars()
        
        self.outputs.pos_actual       = self.outputs.Str(self.widget.pos_actual)
        self.inputs.velocity   = self.inputs.Float(self.widget.input_velocity, default=1.0)
        self.inputs.pos_target = self.inputs.Float(self.widget.input_pos_target)
        
    def update(self, data):
        super().update(data)
        
        #self.input_pos_target.update()
        #self.input_velocity.update() 
        stat = data.stat
        
        pos = stat.pos_name if stat.pos_name else "{:.3f}".format(stat.pos_actual)
            
        self.outputs.pos_actual.set( pos )
    
            
    def connect_device(self, motor, data, more_methods=[]):
        """ Link a device to the widget 
        
        downloader (:class:`pydevmgr.Downloader`): a Downloader object 
        motor (:class:`pydevmgr.Motor`):  Motor device
        altname (string, optional): Alternative printed name for the device
        """        
        super().connect_device(motor, data)
        
        # init some input fields 
        if motor.is_connected():
            self.inputs.velocity.set_input(motor.cfg.velocity.get())
        
        # add more functionality to the dropdown menu, the standards commands are defined in 
        # super().connect_device
        # Here we are adding MOVE ABS MOVE REL and MOVE VEL     
        wa = self.widget.state_action
        # After an command put back the menu to the empty first index
        reset = lambda : wa.setCurrentIndex(0)
        
        wa.addItem("STOP")
        self.actions.add( motor.stop,
                         [], 
                         after=reset, feedback=self.feedback,
                         ).connect_item(wa, wa.count()-1)
        
        wa.addItem("MOVE ABS")
        self.actions.add( motor.move_abs,
                         [self.inputs.pos_target.get, self.inputs.velocity.get], 
                         after=reset, feedback=self.feedback,
                         ).connect_item(wa, wa.count()-1)
                         
        wa.addItem("MOVE REL")
        self.actions.add( motor.move_rel,
                         [self.inputs.pos_target.get, self.inputs.velocity.get], 
                         after=reset, feedback=self.feedback,
                         ).connect_item(wa, wa.count()-1)
                         
        wa.addItem("MOVE VEL")
        self.actions.add( motor.move_vel,
                         [self.inputs.velocity.get], 
                         after=reset, feedback=self.feedback,
                         ).connect_item(wa, wa.count()-1)
        
         
        # Add posname in the list of actions
        list_action = [(name, motor.move_name, [name, self.inputs.velocity.get]) for name in motor.posnames]
        wa.insertSeparator(wa.count())
        
        for i,(name,func, inputs) in enumerate(list_action, start=wa.count()):
            wa.addItem(name)
            self.actions.add(func, inputs, after=reset, feedback=self.feedback).connect_item(wa, i)
                
record_widget_factory("line", "Motor", MotorLine)

