from pydevmgr_elt import Time, DataLink
timer = Time('timer', config=Time.Config( address="opc.tcp://192.168.1.13:4840", prefix="MAIN.timer") )      
import time
try:
    timer.connect()
            
    timer.set_time(None)
    
    data = timer.Data()
    dl = DataLink(timer.stat, data.stat)
    time.sleep(1)
    dl.download()    
    print(data.stat)
finally:
    timer.disconnect()