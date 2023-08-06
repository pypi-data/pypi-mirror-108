from pydevmgr_core import (BaseNode, NodeAlias, BaseInterface,  NodeProperty, 
                           nodeproperty, kjoin, nodealias, NodesReader, 
                           NodesWriter, BaseRpc, buildproperty, download)




msgs = {
'temp001': 10.0
}
# make a dummy Com
class DummyCom:
    def set_msg(self, msg, value):
        msgs[msg] = value 
    def get_msg(self, msg):
        return msgs[msg] 
    def call(self, cmd):
        if cmd == "increase":
            msgs['temp001'] += 1  
            return 0
        return 1  
        
class TestNode(BaseNode):
    def __init__(self, key, com, msg, scale=1):
        super(TestNode, self).__init__(key)
        self._msg = msg
        self._com = com 
        self._scale = scale
    
    @classmethod
    def new(cls, parent, name, msg='', scale=1):
        if not msg:
            raise ValueError("msg shall be defined")
        return cls( kjoin(parent.key, name), parent.com, msg, scale)
    
    @property
    def com(self):
        return self._com
        
    def fget(self):
        return self.com.get_msg(self._msg)*self._scale
    
    def fset(self, value):
        return self.com.set_msg(self._msg, value/self._scale) 

class TestRpc(BaseRpc):
    
    def __init__(self, key, com, cmd):
        super().__init__(key)
        self._cmd = cmd
        self._com = com 
        
    
    @classmethod
    def new(cls, parent, name, cmd=''):
        if not cmd:
            raise ValueError("cmd shall be defined")
        return cls( kjoin(parent.key, name), parent.com, cmd)
    
    @property
    def com(self):
        return self._com
    
    def fcall(self):
        return self.com.call(self._cmd)

@buildproperty(TestNode.prop, ('msg','scale'))        
class TestInterface(BaseInterface):
    
    # test with annotation 
    # the buildproperty decorator will transform the following annotation by: 
    # temp4 = TestNode.prop( 'temp4', msg='temp001', scale=4)  
    temp4 : ('temp001', 4)
    # Or annotation can use dictionaries directly 
    temp5 : {'msg':'temp001', 'scale':5}
    
    Node = TestNode
    
    temp1 = TestNode.prop('temp1', msg='temp001')
    
    def __init__(self, key, com):
        self._key = key 
        self.com = com
                
    #@nodeproperty('temp2')
    @BaseNode.prop('temp2')
    def temp2(self):
        return self.com.get_msg('temp001') * 2
    
    @NodeAlias.prop('temp3', ['temp1'])
    def temp3(self, temp1):
        return temp1 * 3
    
    
    
        
    
itf = TestInterface('mydevice', DummyCom()) 

@nodealias('temp6', [itf.temp2, itf.temp3])
def temp6(t2, t3):
    return t2*t3
    
assert itf.temp1.key == 'mydevice.temp1' 
assert itf.temp1.get() == msgs['temp001']
assert itf.temp2.get() == msgs['temp001']*2
assert itf.temp3.get() == msgs['temp001']*3
assert itf.temp4.get() == msgs['temp001']*4
assert itf.temp5.get() == msgs['temp001']*5

assert temp6.get() == msgs['temp001']**2*2*3

itf.temp1.set(1)
assert msgs['temp001'] == 1

download([itf.temp1, itf.temp2]) == [msgs['temp001'], msgs['temp001']*2]

NodesWriter( {itf.temp1:2} ).write()
assert msgs['temp001'] == 2

print('OK')
#assert tuple(download([itf.temp1,itf.temp2])) ==  (msgs['temp001'], msgs['temp001']*itf.scale)