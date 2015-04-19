import nef
import os
import ca.nengo.model.impl
import ca.nengo.model.neuron.impl
import ca.nengo.model.nef.impl
import ca.nengo.math.impl
import ca.nengo.model.plasticity.impl
import ca.nengo.model.impl.NetworkArrayImpl
import math
import sys
import file2gephi
# import numpy as np
import matrix as mat
import simple_analyze as sa


SEPERATOR_WORD = ','
RETURN = '\n'
__ROOT__ = 'root' # the root prefix of the naming system in nodes
__SPLIT__ = '.'

class NengoAnalyzer:

	def __init__(self,network,name='',dir_name='output',log_name='log',input_list=[]):

		self.__DICT__ = dict()
		self.network = network
		if name != '':
			self.name = name
		else:
			self.name = self.network.network.name
		self.dir_name = dir_name
		self.log_name = log_name
		self.input_list = input_list
		# if log_name == 'log':
		# 	self.log_name = log_name+self.name
		# else:
		# 	self.log_name = log_name

	"""
	function:
		add the specified node's name to the input_list
	"""
	def add_input_node(self,node_name):
		self.input_list.append(node_name)

	"""
	 function:
	   analyze the network. Index every neurons and save in __DICT__
	 paraments:
	   network : the network in nef
	"""
	def analyze_network(self):
		self.__DICT__ = dict()
		c = self._analyze_network_(self.network.network,0,__ROOT__+__SPLIT__)

	def _analyze_network_(self,net,count,prefix):
		# initilize the counter
		__COUNT__ = count

		# for all nodes
		for n in net.getNodes():
			if isinstance( n , ca.nengo.model.impl.EnsembleImpl) :
				for m in range(len(n.nodes)):
					self.__DICT__[prefix+n.name+__SPLIT__+n.nodes[m].name] = __COUNT__
					__COUNT__ = __COUNT__ + 1

			elif isinstance( n , ca.nengo.model.impl.FunctionInput) :
				for f in range(len(n.functions)):
					self.__DICT__[prefix+n.name+__SPLIT__+str(f)] = __COUNT__
					__COUNT__ = __COUNT__ + 1

			elif isinstance( n ,ca.nengo.model.impl.NetworkImpl):
				__COUNT__ = self._analyze_network_(n,__COUNT__,prefix+n.name+__SPLIT__)
			else:
				'=== print found a none type node ' , n.__class__
				self.__DICT__[prefix+n.name] = __COUNT__
				__COUNT__ = __COUNT__ + 1

		return __COUNT__

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
		# if os.path.isfile( self.get_filename_node() )
		fout = open(self.get_filename_node() , 'w')
		fout.write('')
		fout.close()

		open(self.get_filename_node(),'w').close()
		fout = open(self.get_filename_node() , 'w+')
		self._print_nodes_(self.network.network,fout,__ROOT__+__SPLIT__)
		fout.close()

	def _print_nodes_(self,net,fout_,prefix):
		if len(self.__DICT__) <= 0 :
			self.analyze_network()

		if not fout_:
			fout = open(self.get_filename_node() , 'w+')
		else:
			fout = fout_ 

		# for all nodes
		for n in net.getNodes():
			if isinstance( n , ca.nengo.model.impl.EnsembleImpl) :
				print '  [node]',n.name
				for m in n.nodes:
					global_id = str(self.__DICT__[prefix+n.name+__SPLIT__+m.name])
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
				print '  [node]',n.name
				global_id = ''
				element_type = 'simulator'
				model = ''
				_id_class = ''

				if n.name in self.input_list:
					model = 'input'


				for func in range(len(n.functions)):
					str(self.__DICT__[prefix+n.name+__SPLIT__+str(func)])
					if isinstance( n.functions[func] , ca.nengo.math.impl.ConstantFunction):

						model = 'dc_generator'

						amplitude = str(n.functions[func].value)
						_id_class = n.name

						fout.write( global_id + SEPERATOR_WORD \
						+ element_type + SEPERATOR_WORD \
						+ model + SEPERATOR_WORD \
						+ amplitude + SEPERATOR_WORD \
						+ _id_class + RETURN )

					elif isinstance( n.functions[func] , ca.nengo.math.impl.PiecewiseConstantFunction):
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
			elif isinstance( n , ca.nengo.model.impl.NetworkImpl ):
				print '  [node]',n.name
				self._print_nodes_(n,fout,prefix+n.name+__SPLIT__)


		if not fout_:
			fout.close()


	"""
	 function:
	   print the edges in the network
	 paraments:
	   network : the network in nef
	"""
	def print_edges(self):
		open(self.get_filename_edge(),'w').close()
		self._print_edges_(self.network.network,__ROOT__+__SPLIT__)

	def get_origin_node_list(self,origin,prefix):
		result = []
		if isinstance(origin , ca.nengo.model.impl.NetworkImpl.OriginWrapper):
			if not(isinstance(origin.wrappedOrigin,ca.nengo.model.impl.NetworkArrayImpl.ArrayOrigin) \
				or isinstance(origin.wrappedOrigin,ca.nengo.model.impl.NetworkImpl.OriginWrapper)):
				prefix = prefix+origin.node.name+__SPLIT__
			result.extend(self.get_origin_node_list(origin.wrappedOrigin,prefix))
		elif isinstance(origin , ca.nengo.model.impl.NetworkArrayImpl.ArrayOrigin):
			for _origin in origin.nodeOrigins:
				result.extend(self.get_origin_node_list(_origin,prefix+origin.node.name+__SPLIT__))
		elif isinstance(origin , ca.nengo.model.nef.impl.DecodedOrigin):
			if isinstance( origin.node , ca.nengo.model.impl.FunctionInput):
				for f in range(len(origin.node.functions)):
					result.append(self.__DICT__[prefix+origin.node.name+__SPLIT__+str(f)])
			elif isinstance(origin.node , ca.nengo.model.impl.EnsembleImpl):
				n = origin.node
				for m in n.nodes:
					result.append(self.__DICT__[prefix+n.name+__SPLIT__+m.name])
			else:
				print '==== origin node', origin.__class__ , ' type error ===' , origin.node.__class__
		elif isinstance(origin , ca.nengo.model.impl.BasicOrigin):
			if isinstance( origin.node , ca.nengo.model.impl.FunctionInput):
				for f in range(len(origin.node.functions)):
					result.append(self.__DICT__[prefix+origin.node.name+__SPLIT__+str(f)])
			else:
				result.extend([self.__DICT__[prefix+origin.node.name]])
				print '==== origin node', origin.__class__ , ' type error ===' , origin.node.__class__
		elif isinstance(origin , nef.simplenode.SimpleOrigin):
			if isinstance( origin.node , ca.nengo.model.impl.FunctionInput):
				for f in range(len(origin.node.functions)):
					result.append(self.__DICT__[prefix+origin.node.name+__SPLIT__+str(f)])
			else:
				result.extend([self.__DICT__[prefix+origin.node.name]])
				print '==== origin node', origin.__class__ , ' type error ===' , origin.node.__class__
		else:
			print '==== origin type error ===' , origin.__class__
		return result


	def get_termination_node_list(self,termination,prefix):

		result = []
		if isinstance( termination , ca.nengo.model.impl.NetworkImpl.TerminationWrapper):
			if not(isinstance(termination.wrappedTermination,ca.nengo.model.impl.EnsembleTermination)\
				or isinstance(termination.wrappedTermination,ca.nengo.model.impl.NetworkImpl.TerminationWrapper)):
				prefix = prefix+termination.node.name+__SPLIT__
			result.extend(self.get_termination_node_list(termination.wrappedTermination,prefix))
		elif isinstance( termination , ca.nengo.model.impl.EnsembleTermination):
			for _term in termination.nodeTerminations:
				result.extend(self.get_termination_node_list(_term,prefix+termination.node.name+__SPLIT__))
		elif isinstance( termination , ca.nengo.model.nef.impl.DecodedTermination):
			if isinstance(termination.node , ca.nengo.model.impl.FunctionInput):
				result.extend([self.__DICT__[prefix+termination.node.name]])
			elif isinstance( termination.node , ca.nengo.model.impl.EnsembleImpl):
				n = termination.node
				for m in n.nodes:
					result.append(self.__DICT__[prefix+n.name+__SPLIT__+m.name])
			else:
				print '==== termination node type error ===' , termination.node.__class__
		elif isinstance( termination , nef.simplenode.SimpleTermination ):
			result.append(self.__DICT__[prefix+termination.node.name])
		elif isinstance( termination , ca.nengo.model.impl.LinearExponentialTermination):
			result.append(self.__DICT__[prefix+termination.node.name])
		else:
			print '==== termination type error ===' , termination.__class__
			result.append(self.__DICT__[prefix+termination.node.name])
		return result

	def _print_edges_(self,net,prefix):
		if len(self.__DICT__) <= 0 :
			self.analyze_network()

		fout = open(self.get_filename_edge() , 'w+')

		for proj in net.projections:

			p_from = self.get_origin_node_list(proj.origin,prefix)
			p_to = self.get_termination_node_list(proj.termination,prefix)
			print '  [edge]',proj.origin.name,'->',proj.termination.name , ' from' , len(p_from) , 'to' , len(p_to) 

			# the termination
			weights = self.get_weight(proj.origin,proj.termination)

			print 'weight' , len(weights) , len(weights[0])

			for i in range(len(p_from)):
				for j in range(len(p_to)):
					source_id = str(p_from[i])
					target_id = str(p_to[j])
					weight = str(weights[j][i])
					delay = str(proj.termination.tau)

					fout.write( source_id + SEPERATOR_WORD \
					+ target_id + SEPERATOR_WORD \
					+ weight + SEPERATOR_WORD \
					+ delay + RETURN )


	def get_decoders(self,origin):
		# get decoders
		decoders = None
		if isinstance(origin, ca.nengo.model.nef.impl.DecodedOrigin):
			decoders = origin.decoders
		elif isinstance(origin, ca.nengo.model.impl.NetworkArrayImpl.ArrayOrigin):
			for _origin in origin.nodeOrigins:
				_decoder = mat.to_mat(_origin.decoders)
				if decoders == None:
					decoders = _decoder
				else:
					decoders = mat.side_expend(decoders,_decoder)
		elif isinstance(origin, ca.nengo.model.impl.NetworkImpl.OriginWrapper):
			decoders = self.get_decoders(origin.wrappedOrigin)
		elif isinstance(origin, ca.nengo.model.impl.BasicOrigin):
			if isinstance(origin.node, ca.nengo.model.impl.FunctionInput):
				for f in range(len(origin.node.functions)):
					if isinstance(f, ca.nengo.math.impl.ConstantFunction):
						if decoders == None:
							decoders = [[1.0]]
						else:
							decoders = mat.side_expend(decoders,[[1.0]])
			else:
				decoders=mat.ones(1,origin.dimensions)
		else:
			print '===[error]== in' , sys._getframe().f_code.co_name , 'line' , sys._getframe()
			print 'unexpected origin type :' , origin.__class__

		return decoders

	def get_entrans(self,termination):
		entrans = None
		if isinstance(termination,ca.nengo.model.nef.impl.DecodedTermination):
			transforms = termination.transform
			encoders = termination.node.encoders
			entrans = mat.mu(encoders,transforms)
		elif isinstance(termination,ca.nengo.model.impl.LinearExponentialTermination):
			entrans = mat.zeros(1,termination.dimensions)
			for k in range(termination.weights):
				entrans[0][k] = terminations.weights[k]
		elif isinstance(termination,ca.nengo.model.impl.EnsembleTermination):
			terminations = termination.nodeTerminations
			if len(terminations)>0 and isinstance(terminations[0],ca.nengo.model.impl.LinearExponentialTermination):
				for _term in terminations:
					if entrans == None:
						entrans = [_term.weights]
					else:
						entrans = mat.hstack(entrans,[_term.weights])
			elif len(terminations)>0 and isinstance(terminations[0],ca.nengo.model.nef.impl.DecodedTermination):
				for _term in terminations:
					_transform = mat.to_mat(_term.transform)
					node = _term.node
					if isinstance(node,ca.nengo.model.nef.impl.NEFEnsembleImpl):
						_encoder = mat.to_mat(node.encoders)
						_entrans = mat.mu(_encoder,_transform)
						if entrans == None:
							entrans = _entrans
						else:
							entrans = mat.hstack(entrans,_entrans)
					else:
						print '===[error]== in' , sys._getframe().f_code.co_name , 'line' , sys._getframe()
						print 'cannot found node type :' , node.__class__

			elif len(terminations)>0 and isinstance(terminations[0],ca.nengo.model.impl.EnsembleTermination):
				n_neuron = 0
				for i in range(len(terminations)):
					n_neuron = n_neuron + len(terminations[i].nodeTerminations)
				entrans = mat.zeros(n_neuron,termination.dimensions)

				index = 0
				for i in range(len(terminations)):
					_term = terminations[i]
					for j in range(len(_term.nodeTerminations)):
						__term = _term.nodeTerminations[j]
						if isinstance(__term,ca.nengo.model.impl.LinearExponentialTermination):
							for k in range(len(__term.weights)):
								entrans[index+j][k] = __term.weights[k]
						else:
							print '===[error]== in' , sys._getframe().f_code.co_name , 'line' , sys._getframe()
							print 'cannot found sub termination node type :' , __term.__class__
					index = index+len(_term.nodeTerminations)

			else:
				print '===[error]== in' , sys._getframe().f_code.co_name , 'line' , sys._getframe()
				print 'cannot found termination node type :' , terminations[0].__class__
		elif isinstance(termination,ca.nengo.model.impl.NetworkImpl.TerminationWrapper):
			entrans = self.get_entrans(termination.wrappedTermination)
		else:
			print '===[error]===' , 'unexpected termination type' , termination.__class__
			entrans = mat.ones(1,termination.dimensions)
		return entrans

	def get_weight(self,origin,termination):
		# get decoders
		decoders = self.get_decoders(origin)

		# get encoders , transforms
		entrans = self.get_entrans(termination)
		weights = None

		if decoders == None:
			weights = entrans
			# print 'entrans', len(entrans) , len(entrans[0])
		else:
			# print 'decoders' , len(decoders) , len(decoders[0]) , 'entrans', len(entrans) , len(entrans[0])
			weights = mat.mu(entrans,mat.transpose(decoders))

		return weights

	"""
	function:
	   run the simulator and gain the spike information
	"""
	def get_spike(self,time=1.0,isReset=True,isSimpleAnalyze=False):
		self.add_log()
		self.network.run(time)
		self.transform_log(isSimpleAnalyze)
		if isReset:
			self.network.reset()

	"""
	 function:
	   add log to trace the spike of the network(before run)
	 paraments:
	"""

	def add_log(self):
		logname = self.get_log_name()
		if os.path.isfile(logname):
			open(logname,'w').close() # clean a file

		self.log = self.network.log(filename=logname)

		self._add_log_(self.network.network,'')

	def get_log_name(self):
		if self.dir_name != '':
			if not(os.path.isdir(self.dir_name)):
				os.mkdir(self.dir_name)
		return self.dir_name + os.sep + self.log_name + '.csv'

	def _add_log_(self,net,prefix):
		for n in net.getNodes():
			if isinstance(n,ca.nengo.model.impl.EnsembleImpl):
				print 'add to log ', prefix+n.name
				self.log.add_spikes(prefix+n.name,name=prefix+n.name)
			if isinstance(n,ca.nengo.model.impl.NetworkImpl):
				self._add_log_(n,prefix+n.name+__SPLIT__)

	"""
	 function:
	   transform the log from the previous version to right version
	 paraments:
	   log : the name of the log
	"""
	def transform_log(self,filename=None,isSimpleAnalyze=False):
		print '===== begin spike ======'
		if len(self.__DICT__) <= 0 :
			self.analyze_network()

		fin = open(self.get_log_name(),'r')

		fout = None
		if filename == None:
			filename = self.get_filename_spike()
		open(filename,'w').close()
		fout = open(filename,'w+')

		title = fin.readline().split('\n')
		title = title[0].split(',')

		# title[len(title)-1].strip('\n').strip('\r')
		# nodes = []
		# for n in self.network.network.getNodes():
		# 	if isinstance(n,ca.nengo.model.impl.EnsembleImpl):
		# 		nodes.append(n.name)

		for line in fin.readlines():
			con = line.split(',')
			if con[0] != '' and '.' in con[0]:
				time = float(con[0])
			for i in range(1,len(con)):
				sub_con = con[i].split(';')
				for j in range(len(sub_con)):
					if sub_con[j] == '1':
						fout.write( str(self.__DICT__[__ROOT__+__SPLIT__+title[i]+__SPLIT__+'node'+str(j)]) + SEPERATOR_WORD +  str(time) + RETURN )

		fin.close()
		fout.close()

		if isSimpleAnalyze:
			sa.simple_analyze_spike(self.get_filename_spike(),self.dir_name+os.sep+self.log_name+'_sa',self.__DICT__)

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
