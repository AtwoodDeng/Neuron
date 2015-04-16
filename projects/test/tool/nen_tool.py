import nef
import os
import ca.nengo.model.impl
import ca.nengo.model.neuron.impl
import ca.nengo.model.nef.impl
import ca.nengo.math.impl
import ca.nengo.model.plasticity.impl
import math
import sys
import file2gephi


SEPERATOR_WORD = ','
RETURN = '\n'

class NengoAnalyzer:

	def __init__(self,network,name='',dir_name='output',log_name='log'):

		self.__DICT__ = dict()
		self.network = network
		if name != '':
			self.name = name
		else:
			self.name = self.network.network.name
		self.dir_name = dir_name
		self.log_name = log_name

	"""
	 function:
	   analyze the network. Index every neurons and save in __DICT__
	 paraments:
	   network : the network in nef
	"""
	def analyze_network(self):
		self.analyze_network_(self.network)

	def analyze_network_(self,network):
		# initilize the counter
		__COUNT__ = 0
		net = network.network

		self.__DICT__ = dict()

		# for all nodes
		for n in net.getNodes():
			if isinstance( n , ca.nengo.model.impl.EnsembleImpl) :
				for m in range(len(n.nodes)):
					self.__DICT__[n.name+n.nodes[m].name] = __COUNT__
					__COUNT__ = __COUNT__ + 1 


			if isinstance( n , ca.nengo.model.impl.FunctionInput) :
				self.__DICT__[n.name] = __COUNT__
				__COUNT__ = __COUNT__ + 1

		return self.__DICT__

	"""
	 function:
	   get normal file name of the output file
	 paraments:
	"""

	def get_filename(self):
		filename = self.name
		if self.dir_name != '':
			if not(os.path.isdir(self.dir_name)):
				os.mkdir(self.dir_name)
			filename = self.dir_name+ os.sep + filename
		return filename

	def get_filename_node(self,filename=''):
		if filename == '':
			filename = self.get_filename()
		return filename + '_node.csv'

	def get_filename_edge(self,filename=''):
		if filename == '':
			filename = self.get_filename()
		return filename + '_edge.csv'

	def get_filename_spike(self,filename=''):
		if filename == '':
			filename = self.get_filename()
		return filename + '_spike.csv'

	"""
	 function:
	   get the topology of the network
	 paraments:
	   network : the network in nef
	   out_file : name of the network(will be the prefix of the output file)
	   out_dir : name of output directory
	"""
	def get_topology_seperate(self):
		self.get_topology_seperate_(self.network,self.name,self.dir_name)

	def get_topology_seperate_(self,network,out_file,out_dir=''):

		print '====== begin topology ======'

		# filename = out_file
		# if out_dir != '':
		# 	if not(os.path.isdir(out_dir)):
		# 		os.mkdir(out_dir)
		# 	filename = out_dir + os.sep + filename

		# try:
		# 	fout = open(self.get_filename_node(filename),'w')
		# 	__console__ = sys.stdout
		# 	sys.stdout = fout
			# self.print_nodes_(network)
		# 	sys.stdout = __console__
		# finally:
		# 	fout.close()

		# try:
			# fout = open(self.get_filename_edge(filename),'w')
			# __console__ = sys.stdout
			# sys.stdout = fout
			# self.print_edges_(network)
		# 	sys.stdout = __console__
		# finally:
			# fout.close()

		self.print_nodes()
		self.print_edges()

		print '======= end topology ======='


	"""
	 function:
	   print the nodes in the network
	 paraments:
	   network : the network in nef
	"""
	def print_nodes(self):
		self.print_nodes_(self.network)

	def print_nodes_(self,network,):
		if len(self.__DICT__) <= 0 :
			self.analyze_network_(network)

		net = network.network

		fout = open(self.get_filename_node() , 'w+')

		# for all nodes
		for n in net.getNodes():
			if isinstance( n , ca.nengo.model.impl.EnsembleImpl) :
				for m in n.nodes:
					global_id = str(self.__DICT__[n.name+m.name])
					element_type = 'neuron'
					model = str(m.generator.__class__)
					V_reset = ''
					V_th = ''
					E_L = ''
					C_m = ''
					tau_m = ''
					tau_syn = ''
					t_ref = '' 
					_id_class = ''


					if isinstance(m.generator,ca.nengo.model.neuron.impl.LIFSpikeGenerator):
						V_th = str(1)
						V_reset = str(0)
						C_m = str(m.generator.tauRC/1)
						tau_m = str(m.generator.tauRC)
						t_ref = str(m.generator.tauRef)
						_id_class = n.name

					fout.write( global_id + SEPERATOR_WORD \
					+ element_type + SEPERATOR_WORD \
					+ model + SEPERATOR_WORD \
					+ V_reset + SEPERATOR_WORD \
					+ V_th + SEPERATOR_WORD \
					+ E_L + SEPERATOR_WORD \
					+ C_m + SEPERATOR_WORD \
					+ tau_m + SEPERATOR_WORD \
					+ tau_syn + SEPERATOR_WORD \
					+ t_ref + SEPERATOR_WORD \
					+ _id_class + RETURN )


			elif isinstance( n , ca.nengo.model.impl.FunctionInput) :
				global_id = str(self.__DICT__[n.name])
				element_type = 'simulator'
				model = ''
				_id_class = ''


				if isinstance( n.functions[0] , ca.nengo.math.impl.ConstantFunction):
					model = 'dc_generator'
					amplitude = str(n.functions[0].value)
					_id_class = n.name

					fout.write( global_id + SEPERATOR_WORD \
					+ element_type + SEPERATOR_WORD \
					+ model + SEPERATOR_WORD \
					+ amplitude + SEPERATOR_WORD \
					+ _id_class + RETURN )

				elif isinstance( n.functions[0] , ca.nengo.math.impl.PiecewiseConstantFunction):
					model = 'piecewise_generator'
					_id_class = n.name

					fout.write( global_id + SEPERATOR_WORD \
					+ element_type + SEPERATOR_WORD \
					+ model + SEPERATOR_WORD \
					+ ' ' + SEPERATOR_WORD \
					+ _id_class + RETURN )

				else:
					model = 'unknown_generator'
					_id_class = n.name

					fout.write( global_id + SEPERATOR_WORD \
					+ element_type + SEPERATOR_WORD \
					+ model + SEPERATOR_WORD \
					+ '0.0' + SEPERATOR_WORD \
					+ _id_class + RETURN )

					# for test add a '0.0' in the amplitude culumn

		fout.close()


	"""
	 function:
	   print the edges in the network
	 paraments:
	   network : the network in nef
	"""
	def print_edges(self):
		self.print_edges_(self.network)

	def print_edges_(self,network):
		if len(self.__DICT__) <= 0 :
			self.analyze_network_(network)

		fout = open(self.get_filename_edge() , 'w+')

		net = network.network
		for proj in net.projections:

			p_from = []
			p_to = []

			# the origin
			if isinstance( proj.origin.node , ca.nengo.model.impl.FunctionInput ):
				p_from = [self.__DICT__[proj.origin.node.name]]

			if isinstance( proj.origin.node , ca.nengo.model.impl.EnsembleImpl ):
				n = proj.origin.node
				for m in n.nodes:
					p_from.append(self.__DICT__[n.name+m.name])

			# the termination
			if isinstance( proj.termination.node , ca.nengo.model.impl.FunctionInput ):
				p_to = [self.__DICT__[proj.origin.node.name]]
			if isinstance( proj.termination.node , ca.nengo.model.impl.EnsembleImpl ):
				n = proj.termination.node
				for m in n.nodes:
					p_to.append(self.__DICT__[n.name+m.name])

			for i in range(len(p_from)):
				for j in range(len(p_to)):
					source_id = str(p_from[i])
					target_id = str(p_to[j])
					weight = '1.0'
					delay = str(proj.termination.tau)

					if isinstance( proj.termination , ca.nengo.model.nef.impl.DecodedTermination ):
						weight = str(proj.weights[j][i])
					elif isinstance( proj.termination , ca.nengo.model.plasticity.impl.PESTermination ):
						weight = str(proj.termination.nodeTerminations[j].weights[i])

					fout.write( source_id + SEPERATOR_WORD \
					+ target_id + SEPERATOR_WORD \
					+ weight + SEPERATOR_WORD \
					+ delay + RETURN )


	def add_log(self):

		self.logname = self.log_name
		if self.dir_name != '':
			if not(os.path.isdir(self.dir_name)):
				os.mkdir(self.dir_name)
			self.logname = self.dir_name + os.sep + self.logname

		self.log = self.network.log(filename=self.logname)
		for n in self.network.network.getNodes():
			if isinstance(n,ca.nengo.model.impl.EnsembleImpl):
				self.log.add_spikes(n.name)
	"""
	 function:
	   transform the log from the previous version to right version
	 paraments:
	   log : the name of the log
	"""
	def transform_log(self):
		print '===== begin spike ======'
		if len(self.__DICT__) <= 0 :
			self.analyze_network_(network)

		if self.log == None:
			return

		fin = open(self.logname+'.csv','r')

		fout = open(self.get_filename_spike(),'w+')

		# __console__ = sys.stdout
		# sys.stdout = fout

		title = fin.readline().split(',')
		nodes = []
		for n in self.network.network.getNodes():
			if isinstance(n,ca.nengo.model.impl.EnsembleImpl):
				nodes.append(n.name)

		for line in fin.readlines():
			con = line.split(',')
			if con[0] != '' and '.' in con[0]:
				time = int(float(con[0])*1000)
			for i in range(1,len(con)):
				sub_con = con[i].split(';')
				for j in range(len(sub_con)):
					if sub_con[j] == '1':
						fout.write( str(self.__DICT__[nodes[i-1]+'node'+str(j)]) + SEPERATOR_WORD +  str(time) + RETURN )

		# sys.stdout = __console__
		fin.close()
		fout.close()

		print '===== end spike ======'

	"""
	 function:
	   transform the output file to the gephi files
	 paraments:
	"""
	def transform_gephi(self):
		if os.path.exists(self.get_filename_node()):
			file2gephi.node2gephi(self.get_filename_node())
		if os.path.exists(self.get_filename_edge()):
			file2gephi.edge2gephi(self.get_filename_edge())
