import nef
import nps
import random

import tool.simple_analyze as sa 

TEST_TIME = 5
RUN_TIME = 1.0
D=5

net=nef.Network('BasalGanglia') #Create the network object

net.make_input('input',[0]*D) #Create a controllable input function 
                              #with a starting value of 0 for each of D
                              #dimensions
net.make('output',1,D,mode='direct')  
                 #Make a population with 100 neurons, 5 dimensions, and set 
                 #the simulation mode to direct
nps.basalganglia.make_basal_ganglia(net,'input','output',D,same_neurons=False,
    neurons=50)  #Make a basal ganglia model with 50 neurons per action
net.add_to_nengo()

functions = None
for n in net.network.getNodes():
	if n.name == 'input':
		functions = n.functions


import tool.nen_tool as tnt

NA = tnt.NengoAnalyzer(net)
for f in functions:
	f.value = random.randrange(-1.0,1.0)
NA.add_input_node('input')
NA.get_topology_seperate()
NA.transform_gephi()
# for k in range(TEST_TIME):

# 	for f in functions:
# 		f.value = random.randrange(-1.0,1.0)

# 	NA.log_name = 'BAlog' + str(k)
# 	NA.add_log()

# 	net.run(RUN_TIME)
# 	NA.transform_log(isSimpleAnalyze = True)
# 	net.reset()
NA.get_spike(RUN_TIME,isSimpleAnalyze=True)