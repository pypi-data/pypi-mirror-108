from pydevmgr_elt import Downloader, open_device, DataLink
from pydevmgr.devices.motor import MotorStatModel
import time
m = open_device("tins/motor1.yml", "motor1")

dm = MotorStatModel()
D1 = Downloader(m.stat.all_nodes)
dl = DataLink(m.stat, dm)

try:
    m.connect()
    
    t0 = time.time()
    D1.download()
    print("nodes",  (time.time()-t0)*1000 )
    
    t0 = time.time()
    dl._download_from(D1._data)
    print("datalink" , (time.time()-t0)*1000 )
    
finally:
    m.disconnect()
    
