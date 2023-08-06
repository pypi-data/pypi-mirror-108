from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from pydevmgr_elt import open_manager, Downloader
from pydevmgr_qt.manager import ManagerDevicesLinker, Manager


mgr = None
live = True

def main():
    global mgr
    
    #mgr = Manager.from_config('tins/cfgM403.yml', 'fcs')
    #mgr = Manager.from_config('tins/tins.yml', 'fcs', extra_file="tins/tins_pydevmgr.yml")
    mgr = open_manager('tins/tins.yml', 'fcs')
        
    if live:
        mgr.connect()
        #mgr.configure() # configure true OPC-UA the devices
    
    downloader = Downloader()
    def toto(_=None):
        print(len(downloader.data))
        downloader.data.clear()
    #downloader.add_callback(..., toto)
    
    app = QApplication(sys.argv)
    #app.setStyleSheet(style)
    #app.setStyle("Fusion")
    #win = ManagerMainWindow()
    win = Manager()
    ctrl = win.connect(downloader, mgr, win.Data(layout_name="main"))    
    
        
    win.widget.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(downloader.download)
    if live:
        timer.start(200)
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    finally:
        if live and mgr: 
            mgr.disconnect()
