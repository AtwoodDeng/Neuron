'''
Created on May 29, 2014

@author: Francesco Nero
'''

import os
import nengo2nest


#create a directory to store the simulation results. Defaults to current working directory.
#this is where you would also change any settings for the simulation
out_dir = "./neocortical-out"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
nengo2nest.settings.data_path = out_dir

#conversion from nengo happens here. Note that the output is only an abstract representation, and not a nest network yet
network = nengo2nest.network_creator.from_nengo("./nets/NeocorticalMicrocircuitry-withinputs.py")



#label to give the various output files
label = 'Neocortical'

#output to file node, connection and simulation info
nengo2nest.network_creator.nodes_to_file_s(network, label)
# nengo2nest.network_creator.connections_to_file(network, label)
# nengo2nest.settings.to_file(label)


# #print detected neurons, inputs and connections
# print "Neurons"
# print network.get_neurons()
# print "Inputs"
# print network.get_inputs()
# print "Connections"
# for connection in network.get_connections():
#     print connection


#convert from abstract network representation to nest representation
nengo2nest.simulator.setup(network, True, label=label, voltage_watch=network.get_neurons())

#simulation of converted network. Output of simulation results also happens here
nengo2nest.simulator.simulate(50000)