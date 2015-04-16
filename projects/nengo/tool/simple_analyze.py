import sys


K = 10 #iteration time
transform_val = 0.007

class node_info:
	global_id = ''
	ele_type = ''
	model = ''
	v_th = 0.0
	tau_m = 0.0
	amplitude = 0.0
	c_val = 0.0 
	r_val = 0.0
	edges = []
	t_val = 0.0

class edge_info:
	source = ''
	target = ''
	weight = 0.0001
	delay = 0.0001


def simple_analyze(node_file,edge_file,spike_file,out_file):
	print '=== simple analyze ===='
	print '[Input file] :' , node_file , edge_file , spike_file


	nodes = dict()
	edges = dict()

	fnode=open(node_file,'r')

	for line in fnode.readlines():
		words = line.split(',')
		global_id = words[0]
		ele_type = words[1]
		model = words[2]

		node = node_info()
		node.global_id = global_id
		node.ele_type = ele_type
		node.model = model
		node.edges = []

		if ele_type == 'neuron':
			node.v_th = float(words[4])-float(words[3])
			node.tau_m = float(words[7])
		elif model == 'dc_generator':
			node.amplitude = float(words[3])
		elif model == 'input':
			node.amplitude = 1.00
		nodes[global_id] = node


	fspike = open(spike_file,'r')
	for line in fspike.readlines():
		words = line.split(',')
		nodes[words[0]].t_val = nodes[words[0]].t_val + 1

	fedge = open(edge_file , 'r')
	for line in fedge.readlines():
		words = line.split(',')
		source = words[0]
		target = words[1]
		weight = float(words[2])
		delay = float(words[3])

		edge = edge_info()
		edge.source = source
		edge.target = target
		edge.weight = weight 
		edge.delay = delay

		nodes[target].edges.append(edge)

	for t in range(K):
		for node in nodes.values():
			if node.model == 'dc_generator':
				node.r_val = node.amplitude
			elif node.ele_type == 'neuron' :
				node.c_val = 0
				for edge in node.edges:
					node.c_val = node.c_val + get_connection_value(nodes[edge.source],nodes[edge.target],edge)
				cval2rval(node)

	if not(out_file.endswith('.csv')):
		out_file = out_file + '.csv'
	fout = open(out_file,'w+')

	max_t_val = 0.0
	max_r_val = 0.0
	for node in nodes.values():
		if node.ele_type == 'neuron':
			if node.t_val > max_t_val:
				max_t_val = node.t_val
			if node.r_val > max_r_val:
				max_r_val = node.r_val

	for i in range(len(nodes)):
		node = nodes[str(i)]
		if node.ele_type == 'neuron':
			fout.write(node.global_id+','+str(node.r_val/max_r_val)+','+str(node.t_val/max_t_val)+'\n')
		else:
			fout.write(node.global_id+','+str(0.0)+','+str(0.0)+'\n')

	print '==== End simeple analyze ==='

def simple_analyze_spike(spike_file,out_file,n_dict=None):
	fin = open(spike_file,'r')
	nodes = dict()
	lines = fin.readlines()

	__COUNT__ = 0
	for line in lines:
		words = line.split(',')
		time  = float(words[1].strip('\n').strip('\r'))
		if words[0] in nodes.keys():
			nodes[words[0]] = nodes[words[0]] + 1
		else:
			nodes[words[0]] = 1

		# if time > (__COUNT__+1)*(step):
		# 	fout = open(out_file+str(__COUNT__)+'.csv','w+')
		# 	__COUNT__ = __COUNT__ + 1

		# 	n_node = len(nodes)
		# 	if not(n_dict==None):
		# 		n_node = len(n_dict)

		# 	print 'n_node',n_node
		# 	for k in range(n_node):
		# 		if str(k) in nodes.keys():
		# 			fout.write(str(k)+','+str(nodes[str(k)])+'\n')
		# 		else:
		# 			fout.write(str(k)+',0\n')
		# 	fout.close()
		# 	nodes = dict()	
	fin.close()

	fout = open(out_file+str(__COUNT__)+'.csv','w+')
	__COUNT__ = __COUNT__ + 1
	n_node = len(nodes)
	if not(n_dict==None):
		n_node = len(n_dict)

	for k in range(n_node):
		if str(k) in nodes.keys():
			fout.write(str(k)+','+str(nodes[str(k)])+'\n')
		else:
			fout.write(str(k)+',0\n')


	fout.close()


def simple_analyze_spike_filter(spike_file,out_file='',n_dict=None):
	fin = open(spike_file,'r')
	lines = fin.readlines()
	nodes = dict()
	for line in lines:
		words = line.split(',')
		time  = float(words[1].strip('\n').strip('\r'))
		if words[0] in nodes.keys():
			nodes[words[0]].append(time)
		else:
			nodes[words[0]]= [time]

	fin.close()

	if out_file == '':
		out_file = spike_file[:-4]+'_filter.csv'
	if not(out_file.endswith('.csv')):
		out_file = out_file + '.csv'
	fout = open(out_file,'w+')

	if not(n_dict==None):
		n_node = len(n_dict)
		for k in range(n_node):
			if str(k) in nodes.keys():
				fout.write(str(k))
				for i in range(len(nodes[str(k)])):
					fout.write(','+str(nodes[str(k)][i]))
				fout.write('\n')
			else:
				fout.write(str(k)+'\n')
	else:
		for node in nodes:
			fout.write(node)
			for i in range(len(nodes[node])):
				fout.write(','+str(nodes[node][i]))
			fout.write('\n')

	import pylab as pl
	## plot ###
	MAX_TIME = 0.10
	for node in nodes:
		x = []
		for _time in nodes[node]:
			# if _time>0.8 and _time<0.9:
			x.append(_time)
		y = [float(node) for i in range(len(x))]
		pl.plot(x,y,'ob')

	# pl.xlim(0.0,MAX_TIME)
	pl.show()

	## plot ###

	fout.close()



def get_connection_value(source,target,edge):
	connect_weight = edge.weight / edge.delay
	source_weight = source.r_val
	return connect_weight * source_weight * transform_val

def cval2rval(node):
	node.r_val = (node.c_val / node.tau_m + node.r_val)/2

if __name__ == '__main__':
	simple_analyze(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])	
	# simple_analyze_spike_filter(sys.argv[1])
