import nef
import math
import random

neurons=200
segments=3
feedback_pstc=0.3
feedback_scale=1.1
couple_weight=0.2 #set connection weights to make sure that coupling is maintained at least at the minimum
segment_pstc=0.3
period=1
omega=(math.pi*2)/period # omega =10 worked well for the starting paramaters

# Code to simulate the coupled oscillations produced by the motor neurons of the lamprey - in 3 vertebrae segments
# Running nengo GUI allows control of direction (direction) as well as speed (omega)
# Weights displayed FYI only (saved in file in same directory) are the connection weights produced by Nengo between segments

random.seed(12)

#specify vector that defines position of neuron on the cartisian plane
#to turn right stimulate the left side of the oral hood 

encoders=[]
for i in range(neurons): 
	#colon for anytime indent
	theta = i*2*math.pi/neurons
	encoders.append([math.sin(theta),math.cos(theta),random.uniform(-1,1)]) 

def control(v):
	x=v[0]
	y=v[1]
	w=v[2]*20
	return [x*feedback_scale + w*feedback_pstc*y,-w*feedback_pstc*x + y*feedback_scale]
		
# x and y need to be separated - and managed separately - when it reaches a prefered direction vector for that neuron - it should spike.. 
	
net = nef.Network('Lamprey',quick=True)
input_w=net.make_input('Omega',[1])
direction=net.make_input('Direction', [0])

for s in range(segments):
		segment = net.make('s%d'%s,neurons=neurons,dimensions=3,tau_rc=0.02,tau_ref=0.002,radius=1.4, 
                encoders=encoders, intercept=(0.2,0.9),max_rate=(100,200)) # (tau_ref/rc = mseconds) 2 neurons per segment - coupled neurons doing opposite opperations intercepts to be played with later.. close to theta origin
		net.connect(segment,segment,pstc=feedback_pstc,func=control,index_post=[0,1])
		net.connect(input_w,segment,index_post=[2])
		net.connect(direction,segment,index_post=[2])
    
for s in range(segments-1):
    net.connect('s%d'%s,'s%d'%(s+1),pstc=segment_pstc,index_pre=[0,1],index_post=[0,1],weight=couple_weight)
    
input=net.make_input('Input',[0,0])
net.connect(input,'s0',index_post=[0,1],pstc=0.01)

data=file('nengo_weight_values.py','w')    # open a file for writing

#A=net.make('A', neurons=100, dimensions=1, max_rate=(20,50),radius=1, intercept=(-.80,.80))
#B=net.make('B', neurons=120, dimensions=1, max_rate=(20,50),radius=1, intercept=(-.80,.80))

node_a = net.network.getNode('s1')
node_b = net.network.getNode('s2')

def get_weights(node_a, node_b, origin_name='X'):
  dec=node_a.getOrigin(origin_name).getDecoders()
  a = array([ x[0] for x in dec ])
  a = reshape(a, (len(a),1))
  b = [node_b.nodes[i].scale*node_b.encoders[i][0] for i in range(len(node_b.encoders))]    # 10 is tau_syn --> normalization ???
  
  temp = a*b
#   print a
#   print b
#   print a*b
  
  out = "["
  for t in temp:
	out += "%s,\n" % list(t)
	out += "]"
	return(out)

data.write('weights=%s\n' % get_weights(node_a,node_b))



# net.view()
data.close()



import tool.nen_tool as tnt
NA = tnt.NengoAnalyzer(net)
NA.add_log()
net.run(1.0)

NA.get_topology_seperate()
NA.transform_gephi()
NA.transform_log()

