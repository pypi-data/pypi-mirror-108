from pydevmgr_elt import open_device, wait, upload, download

# quick test, this not test all functionality but just to make sure that the structure of 
# the code is still working 

drot = open_device("tins/drot1.yml")

drot.stat
drot.cfg
drot.rpc

###
# test connected

try: 
    drot.connect()
    drot.configure()
    
    d = {}
    download(drot.cfg.all_native_nodes, d)
    upload( d )
    
    print(drot.stat.pos_actual.key, drot.stat.pos_actual.get())
    wait( drot.reset() )
    wait( drot.init() )
    assert drot.stat.is_ready.get()
    wait( drot.enable() )
    wait( drot.move_abs(1.0, 10.0))
    assert abs(drot.stat.pos_actual.get()-1.0)<0.001
    
    drot.cfg.init_seq1_action.set(0)
    drot.start_track('SKY')
finally:
    drot.disconnect()

print("OK")