from PyQt5 import  uic
from .io import find_ui
from pydevmgr_elt import NodeVar
from .device_line import DeviceLineUi, DeviceLine
from .base import record_widget_factory


# ################################################

class AdcLineStatData(DeviceLine.Data.StatData):
    track_mode_txt : NodeVar[str] = ""

class MotorCtrStatData(DeviceLine.Data.StatData):
    pos_actual: NodeVar[float] = 0.0
    pos_error:  NodeVar[float] = 0.0
    pos_target: NodeVar[float] = 0.0
    vel_actual: NodeVar[float] = 0.0

class MotorCtrData(DeviceLine.Data):
    StatData =  MotorCtrStatData
    
    stat: StatData = StatData()  
    
class AdcLineData(DeviceLine.Data):
    StatData = AdcLineStatData
    MotorData = MotorCtrData
    
    stat: StatData = StatData()
    motor1: MotorData = MotorData()
    motor2: MotorData = MotorData()

# ################################################


class AdcLineUi(DeviceLineUi):
    def init_ui(self):
        uic.loadUi(find_ui('adc_line_frame.ui'), self)

class AdcLine(DeviceLine):    
    Data = AdcLineData
    Widget = AdcLineUi  
    
    def init_vars(self):
        super().init_vars()
        w = self.widget 
        self.outputs.motor1_pos_actual = self.outputs.Float(w.motor1_pos_actual, fmt="%.3f")
        self.outputs.motor2_pos_actual = self.outputs.Float(w.motor2_pos_actual, fmt="%.3f")
        self.outputs.track_mode = self.outputs.Str(w.track_mode_txt)
        
        #self.inputs.velocity = self.inputs.Float(w.input_velocity, default=1.0)
        self.inputs.angle = self.inputs.Float(w.input_angle, default=0.0)
        
    def update(self, data: AdcLineData):
        super().update(data)
        self.outputs.motor1_pos_actual.set(  data.motor1.stat.pos_actual ) 
        self.outputs.motor2_pos_actual.set(  data.motor2.stat.pos_actual ) 
        self.outputs.track_mode.set(data.stat.track_mode_txt)
                
    def connect_device(self,  adc, data):
        super().connect_device(adc, data)
        
        wa = self.widget.state_action
        
        wa.insertSeparator(wa.count())
        reset = lambda : wa.setCurrentIndex(0)
        
        wa.addItem("MOVE ANGLE")
        self.actions.add( adc.move_angle,
                         [self.inputs.angle.get], 
                         after=reset
                         ).connect_item(wa, wa.count()-1)
        
        wa.addItem("START TRACK")
        self.actions.add( adc.start_track,
                         [self.inputs.angle.get], 
                         after=reset
                         ).connect_item(wa, wa.count()-1)
        
        wa.addItem("STOP TRACK")
        self.actions.add( adc.start_track,
                         [], 
                         after=reset
                         ).connect_item(wa, wa.count()-1)
                
           

record_widget_factory("line", "Adc", AdcLine)
