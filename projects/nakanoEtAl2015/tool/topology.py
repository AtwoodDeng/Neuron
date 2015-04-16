import nest
import sys

### 
# features that should be print by get_topology()
### 
# features of node
feature_normal_node = ['global_id' , 'element_type', 'model']
feature_neuron = ['global_id' , 'element_type', 'model' , 'V_reset' , 'V_th' , 'E_L' , 'C_m' ]
# element filters of node
NEURON_ONLY = ['neuron']
ALL_TYPE = ['neuron','recorder','stimulator']
# features of edge
feature_edge = ['source' , 'target' , 'weight' , 'delay']

SEPERATOR_WORD = ','
SEPERATOR_LINE = ''

PRINT_NUMBER = False


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
		f_out = open(out_file+'.csv','w')
		__console__ = sys.stdout
		sys.stdout = f_out
		print_topology()
		sys.stdout=__console__

	print '======= Topology End ========'
		
###########
# function:
#   output the struction of the nest network
# Parameter:
#   out_file : the name of the output file(output to the console if out == 'nil')
###########
def get_topology_seperate(out_file):

	# print '==== Begin Topology ====='

	print '======= Topology Seperate Begin ======='

	f_node = open(out_file+'_node.csv','w')
	f_edge = open(out_file+'_edge.csv','w')
	__console__ = sys.stdout

	sys.stdout = f_node
	print_topology_node()
	sys.stdout = f_edge
	print_topology_edge()

	sys.stdout=__console__

	print '======= Topology Seperate End ========'


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
		if i == len(filters) -1 :
			out +=  str(d[filters[i]]) + SEPERATOR_LINE
		else:
			out += str(d[filters[i]]) + SEPERATOR_WORD
	return out

###########
# function:
#   print the topology information of the nest network
###########
def print_topology():
	print_topology_node()
	print_topology_edge()

###########
# function:
#   print the node information of the nest network
###########
def print_topology_node():
	kernel_status = nest.GetKernelStatus()

	# nodes
	sta_node = nest.GetStatus(tuple(range(kernel_status['network_size'])))	
	if PRINT_NUMBER:
		print len(sta_node)
	for i in range(len(sta_node)):
		print sta2str_node(sta_node[i])

###########
# function:
#   print the edge information of the nest network
###########
def print_topology_edge():
	connections = nest.GetConnections()

	# connections
	sta_edge = nest.GetStatus(connections)
	if PRINT_NUMBER:
		print len(sta_edge)

	for i in range(len(sta_edge)):
		print sta2str_edge(sta_edge[i])
