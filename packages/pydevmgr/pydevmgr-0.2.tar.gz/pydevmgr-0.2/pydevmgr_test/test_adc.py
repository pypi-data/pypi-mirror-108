from pydevmgr_elt import open_device, wait

# quick test, this not test all functionality but just to make sure that the structure of 
# the code is still working 

adc = open_device("tins/adc1.yml")

adc.stat
adc.cfg
adc.rpc

###
# test connected

try: 
    adc.connect()
    adc.configure()
    
    print(adc.motor1.stat.pos_actual.key, adc.motor1.stat.pos_actual.get())
    print('reset');wait( adc.reset() )
    print('init');wait( adc.init() )
    print('enable');wait( adc.enable() )
    print('move_abs');wait( adc.move_abs(1, 1.0, 10.0))
    assert abs(adc.motor1.stat.pos_actual.get()-1.0)<0.01
    
    adc.start_track()
finally:
    adc.disconnect()

print("OK")