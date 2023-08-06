from pydevmgr_elt import CcsSim, DataLink
ccs = CcsSim('ccs', config=CcsSim.Config( address="opc.tcp://192.168.1.13:4840", prefix="MAIN.ccs_sim") )      

try:
    ccs.connect()
    ccs.set_coordinates(122345.00, 240000.0, 2000.0)
    data = ccs.Data()
    dl = DataLink(ccs.stat, data.stat)
    
    dl.download()
    print(ccs.stat.ra.get())
    print(data.stat)
finally:
    ccs.disconnect()
    