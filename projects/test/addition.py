# import extract
import nef
import ca.nengo.model.impl
import tool.nen_tool as tnt

N_neuron = 100

# print '===== begin addition ====='
net=nef.Network('Addition') #Create the network object

net.make_input('inputA',[0])  #Create a controllable input function 
                               #with a starting value of 0
net.make_input('inputB',[0])  #Create another controllable input 
                               #function with a starting value of 0
                  
# print '===== net ====='             
net.make('A',N_neuron,1) #Make a population with 100 neurons, 1 dimension
net.make('B',N_neuron,1) #Make a population with 100 neurons, 1 dimension
net.make('C',N_neuron,1) #Make a population with 100 neurons, 1 dimension

net.connect('inputA','A') #Connect all the relevant objects
net.connect('inputB','B')
net.connect('A','C')
net.connect('B','C')

# print '===== extract ====='
# extract.extract(net, filename='add.txt') 

# log = net.log(filename='log')

# log.add('input A',tau=0)
# log.add('A')
# log.add('B')
# log.add('C')
# log.add_spikes('inputA')
# log.add_spikes('inputB')

# log.add_spikes('A')
# log.add_spikes('B')
# log.add_spikes('C')

# print '===== node ========'
# nn = net.network
# for n in nn.getNodes():
# 	print n.name
# 	if isinstance( n , ca.nengo.model.impl.EnsembleImpl) :
# 		for m in n.nodes:
# 			print m.generator

# print '===== projections ========'
# for p in nn.projections:
# 	print p.origin.node.name , p.termination.node.name
# 	print p.weights
# 	print p.termination.tau

# net.add_to_nengo()

NA = tnt.NengoAnalyzer(net)
NA.add_log()
net.run(1.0)

NA.get_topology_seperate()
NA.transform_gephi()
NA.transform_log()



# print log.filename, '========'
# log.write_data()


# net.log('test')

 
