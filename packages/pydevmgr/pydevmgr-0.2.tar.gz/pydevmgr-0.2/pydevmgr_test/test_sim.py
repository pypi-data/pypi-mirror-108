from pydevmgr_elt import * 
from pydevmgr.base.uacom import UaSimCom, SimNodeData
from pprint import pprint
import threading

def init():
    print('init')

def gen_sim_dict(ns=4, s=""):
    d =  {
        'stat.nState' :    0,
        'stat.nSubstate' : 0,
        'stat.nStatus' :   0,
        'stat.bLocal' :  False,
        'stat.lrIntensity' : 0.0,
        'stat.nErrorCode' : 0,
        'stat.bCheckTimeLeft' : False,
        'stat.nTimeLeft' : 0.0,       
    }
    out = {}
    for k,v in d.items():
        nid = 'ns={};s={}'.format(ns, kjoin(s,k))
        out[nid] = SimNodeData(value=v, nodeid=nid)        
    
    handler = Lamp('_simlamp', uacom=UaSimCom( out ), prefix=s)
    def init():
        handler.stat.state.set(1)
        return 0
        #k = 'stat.nState'
        #nid = 'ns={};s={}'.format(ns, kjoin(s,k))
        #out[nid].value = 1
        #return 0
    def switchOn(i,t):
        handler.stat.intensity.set(i)
        def turnoff():
            print("switching off")
            handler.stat.intensity.set(0.0)
        threading.Timer(t.Value, turnoff).start()
        return 0    
            
        
    nid =  f'ns={ns};s={s}'   
    out[nid] =  SimNodeData(nodeid=nid, methods={
        f'{ns}:RPC_Init' :init,
        f'{ns}:RPC_On' :switchOn, 
    })    
    return out 

l = Lamp('lamp', uacom=UaSimCom( gen_sim_dict(s="MAIN.Lamp1") ), prefix="MAIN.Lamp1")
assert l.stat.state.get() == 0
l.rpc.rpcInit.call()
assert l.stat.state.get() == 1
l.rpc.rpcSwitchOn.call(80, 5)

