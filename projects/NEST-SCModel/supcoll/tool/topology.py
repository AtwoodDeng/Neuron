import nest
import sys

### 
# features that should be print by get_topology()
### 
# features of node
feature_normal_node = ['global_id' , 'element_type', 'model']
feature_neuron = ['global_id' , 'element_type', 'model' , 'V_reset' , 'V_th' , 'V_m' , 'E_L' , 'C_m']
# element filters of node
NEURON_ONLY = ['neuron']
ALL_TYPE = ['neuron','recorder','stimulator']
# features of edge
feature_edge = ['source' , 'target' , 'weight' , 'delay']


###########
# function:
#   output the struction of the nest network
# Parameter:
#   out_file : the name of the output file(output to the console if out == 'nil')
###########
def get_topology(out_file='nil'):

	# print '==== Begin Topology ====='

	print '======= Topology Begin ======='

	if out_file == 'nil':
		print_topology()
	else:
		f_out = open(out_file,'w')
		__console__ = sys.stdout
		sys.stdout = f_out
		print_topology()
		sys.stdout=__console__

	print '======= Topology End ========'
		

###########
# function:
#   change the data of node's status to string
# Parameter:
#   sta : the status of node
# output :
#   the string of the features in the node(relating to feature_node)
###########
###########

def sta2str_node(sta):
	if sta['element_type'] == 'neuron':
		return filterFromDic(sta,feature_neuron)
	else:
		return filterFromDic(sta,feature_normal_node)

###########
# function:
#   change the data of edge's status to string
# Parameter:
#   sta : the status of edge
# output :
#   the string of the features in the edge(relating to feature_edge)
###########
def sta2str_edge(sta):
	return filterFromDic(sta,feature_edge)

###########
# function:
#   filter the required element form a dictionary
# Parameter:
#   d : the dictionary
#   filters : the filter 
# output :
#   the string of the filtered elements in the dictionary
###########
def filterFromDic(d,filters):
	out = ""
	for i in range(len(filters)):
		out += str(d[filters[i]]) + " "
	return out

###########
# function:
#   print the topology information of the nest network
# Parameter:
#   d : the dictionary
#   filters : the filter 
# output :
#   the string of the filtered elements in the dictionary
###########
def print_topology():

	kernel_status = nest.GetKernelStatus()
	connections = nest.GetConnections()

	# nodes
	sta_node = nest.GetStatus(tuple(range(kernel_status['network_size'])))	
	print len(sta_node)
	for i in range(len(sta_node)):
		print sta2str_node(sta_node[i])

	# connections
	sta_edge = nest.GetStatus(connections)
	print len(sta_edge)
	for i in range(len(sta_edge)):
		print i , sta2str_edge(sta_edge[i])
