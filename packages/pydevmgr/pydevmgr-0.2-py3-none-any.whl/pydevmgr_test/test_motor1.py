from pydevmgr_elt import open_device, wait, download, upload

# quick test, this not test all functionality but just to make sure that the structure of 
# the code is still working 

m1 = open_device("tins/motor1.yml")

m1.stat
m1.cfg
m1.rpc

###
# test connected

try: 
    m1.connect()
    m1.configure(velocity=100)
    d = {}
    download(m1.cfg.all_native_nodes, d)
    upload( d )
    
    m1.cfg.init_seq1_action.set(0) # quick init 
    
    print(m1.stat.pos_actual.key, m1.stat.pos_actual.get())
    wait( m1.reset() )
    wait( m1.init() )
    wait( m1.enable() )
    wait( m1.move_abs(1.0, 10.0))
    
    assert abs(m1.stat.pos_actual.get()-1.0)<0.01
    
    
finally:
    m1.disconnect()

print("OK")