from PyQt5 import QtGui, QtCore  # (the example applies equally well to PySide)
import pyqtgraph as pg
import numpy as np 
import sys 
from pydevmgr_elt import open_device, Downloader, DequeNode, Prefixed, local_utc, local_time
from pydevmgr_qt import get_widget_constructor


## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

plots = {'pos': pg.PlotWidget(title='pos'), 
         'vel': pg.PlotWidget(title='velocity'), 
         'time': pg.PlotWidget(title='tick tack'), 
         }

ctrl = get_widget_constructor("ctrl", "Motor")()
clear_btn = QtGui.QPushButton('Clear')
maxlen = QtGui.QLineEdit('500')
## Create a grid layout to manage the widgets size and position
layout = QtGui.QVBoxLayout()
w.setLayout(layout)

layout.addWidget(ctrl)
layout.addWidget(plots['pos'])  # plot goes on right side, spanning 3 rows
layout.addWidget(plots['vel'])  # plot goes on right side, spanning 3 rows
layout.addWidget(plots['time'])  # plot goes on right side, spanning 3 rows
layout.addWidget(clear_btn)
layout.addWidget(maxlen)

def plot_update(data):
        
    n = len(data['plot_data'])
    if not n: return None
    
    time, pos, vel = zip(*data['plot_data'])
    time = np.asarray(time)-data['start_time']
    plot = plots['pos']
    plot.clear()
    plot.plot( time, pos)
    
    plot = plots['vel']
    plot.clear()
    plot.plot(time, vel)
    
    plot = plots['time']
    plot.clear()
    plot.plot(time[:-1], time[1:]-time[:-1] )
    

if __name__ == "__main__":
    ## Display the widget as a new window
    w.show()
    motor = open_device("tins/motor1.yml")
    data = {'start_time':local_time.get()}
    
    try:
        motor.connect()
        fifo = DequeNode( "plot_data", [local_time, motor.stat.pos_actual, motor.stat.vel_actual], 500)
        
        downloader = Downloader( [fifo], data, callback=plot_update)
        ctrl.link_device(downloader, motor)
        
        clear_btn.clicked.connect( lambda : fifo.clear(int(maxlen.text())) )
        
        timer = QtCore.QTimer()
        timer.timeout.connect(downloader.download)
        timer.start(100)
        app.exec_()
    finally:
        motor.disconnect()
