import sys
sys.path.append('/Users/atwood/tem/Neu/projects/nengo')


from spa import *
import nef

dimensions=24

import Source
class Rules:
    
    def ruleYM(vision_turn = 'MYMOVE',mode='-DO_ANY'): # Check for your move
        set(attention = 'E', memory = 'BLANK', move = 'DOANY', mode = 'DO_ANY')
          
    #Do Any Move
    def ruleDA51(mode='DO_ANY',attention='E*2',vision='BLANK*2',scale=1.0/3):
        set(motor='E',move='DOANY',attention='E')
    def ruleDA52(mode='DO_ANY',attention='E*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention='A')
    def ruleDA11(mode='DO_ANY',attention='A*2',vision='BLANK*2',scale=1.0/3):
        set(motor='A',move='DOANY',attention='A')
    def ruleDA12(mode='DO_ANY',attention='A*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention='C')
    def ruleDA31(mode='DO_ANY',attention='C*2',vision='BLANK*2',scale=1.0/3):
        set(motor='C',move='DOANY',attention = 'C')
    def ruleDA32(mode='DO_ANY',attention='C*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention='G')
    def ruleDA71(mode='DO_ANY',attention='G*2',vision='BLANK*2',scale=1.0/3):
        set(motor='G', move='DOANY', attention = 'G')
    def ruleDA72(mode='DO_ANY',attention='G*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention='J')    
    def ruleDA91(mode='DO_ANY',attention='J*2',vision='BLANK',scale=1.0/3):
        set(motor='J', move='DOANY',attention='J')
    def ruleDA92(mode='DO_ANY',attention='J*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention = 'B')
    def ruleDA21(mode='DO_ANY',attention='B*2',vision='BLANK',scale=1.0/3):
        set(motor='B',move='DOANY',attention='B')
    def ruleDA22(mode='DO_ANY',attention='B*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention='D')
    def ruleDA41(mode='DO_ANY',attention='D*2',vision='BLANK',scale=1.0/3):
        set(motor='D',move='DOANY', attention='D')
    def ruleDA42(mode='DO_ANY',attention='D*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention='F')
    def ruleDA61(mode='DO_ANY',attention='F*2',vision='BLANK',scale=1.0/3):
        set(motor='F', move='DOANY',attention='F')
    def ruleDA62(mode='DO_ANY',attention='F*2',vision='X+O-BLANK',scale=1.0/3):
        set(attention='H')
    def ruleDA81(mode='DO_ANY',attention='H*2',vision='BLANK',scale=1.0/3):
        set(motor='H', move='DOANY',attention='H')
    def ruleDA82(mode='DO_ANY',attention='H*2',vision='X+O-BLANK',scale=1.0/3):
        set(move = 'NOMOVE')
    

class SimpleModule(module.Module):
    def __init__(self,klass,*args,**params):
        self.klass=klass
        module.Module.__init__(self,**params)
        self.args=args
        self.params=params
    def create(self):
        self.node=self.klass(*self.args,**self.params)
        self.net.add(self.node)
        self.node.module=self
        self.node.spa=self.spa
        if hasattr(self.node,'create'):
            self.node.create()
    def connect(self):
        if hasattr(self.node,'connect'):
            self.node.connect()
            
game=Source.TicTacToe()            
           
class Vision(nef.SimpleNode):
    def origin_item(self):
        if self.t_start<=0: return [0]*dimensions
        
        location=model.attention.net.network.getNode('buffer').getOrigin('X').getValues().getValues()
        
        vocab=model.vocab('vision')
        similarity=list(vocab.dot(location))
        index=similarity.index(max(similarity))
        symbol=vocab.keys[index]
        
        if symbol in 'ABCDEFGHJ':
            # figure out item at location
            item=game.getSymbolAt('ABCDEFGHJ'.index(symbol))
            #System.out.println("In Python "+item)
            if item=='X': return vocab.parse('X').v
            elif item=='O': return vocab.parse('O').v
            else : return vocab.parse('BLANK').v
        else:
            return [0]*dimensions
            
    def origin_current_turn(self):
        if self.t_start<=0: return [0]*dimensions
        vocab=model.vocab('vision')
        if game.getCompMove()==1:
            return vocab.parse('MYMOVE').v
        else:    
            return vocab.parse('-MYMOVE*10').v
        
        
    def create(self):        
        self.module.add_source(self.getOrigin('item'))        
        self.module.add_source(self.getOrigin('current_turn'),'turn')        
     
class Motor(nef.SimpleNode):
    pstc=0.05
    def termination_move(self,x,dimensions=dimensions):
        location=model.attention.net.network.getNode('buffer').getOrigin('X').getValues().getValues()
        vocab=model.vocab('motor')
        similarity=list(vocab.dot(location))
        #print similarity
        if max(similarity)<0.3: return
        index=similarity.index(max(similarity))
        symbol=vocab.keys[index]        
        #print symbol
        if symbol in 'ABCDEFGHJ':
            index='ABCDEFGHJ'.index(symbol)
            if symbol=='A': game.setIndex(index)
            if symbol=='B': game.setIndex(index)
            if symbol=='C': game.setIndex(index)
            if symbol=='D': game.setIndex(index)
            if symbol=='E': game.setIndex(index)
            if symbol=='F': game.setIndex(index)
            if symbol=='G': game.setIndex(index)
            if symbol=='H': game.setIndex(index)
            if symbol=='J': game.setIndex(index)
        else:
            game.setIndex(-1)        
        

class MyModel(SPA):
    dimensions=dimensions
    align_hrrs=True
    
    attention=Buffer()
    mode=Buffer()
    memory=Buffer()
    move=Buffer()
    vision=SimpleModule(Vision,'vision')        
    #motor=SimpleModule(Motor,'motor')
    #vision=Buffer(feedback=0)
    motor=Buffer(feedback=0)   
    BG=BasalGanglia(Rules())
    thal=Thalamus(BG)
    #input=Input(1,attention='A',mode='DO_ANY*2')

model=MyModel('TicTacToe')

motor2=model.net.add(Motor('motor2'))
model.net.connect(model.net.network.getNode('motor').getOrigin('motor'),motor2.getTermination('move'))

import tool.nen_tool as tnt
NA = tnt.NengoAnalyzer(model.net)
NA.get_topology_seperate()
NA.transform_gephi()

TEST_TIME  =10
RUN_TIME = 1.0
for k in range(TEST_TIME):
    NA.log_name = 'TTT' + str(k)
    NA.add_log()
    NA.network.run(RUN_TIME)
    NA.transform_log(isSimpleAnalyze=True)