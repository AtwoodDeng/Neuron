import nest
import sys
import os

SEPERATOR_WORD = ','
SEPERATOR_LINE = ''

class SpikeAnalyzer:

	###########
	# function:
	#   create spike detectors and connect with all neurons and spike generators
	###########
	def Init(self):
		# get the basic information of the network
		kernel_status = nest.GetKernelStatus()
		num_node = kernel_status['network_size']
		nodes_status = nest.GetStatus(tuple(range(num_node)))

		# connect the node to the spike detector
		self.spike_detectors = nest.Create('spike_detector', num_node)
		self.spike_dict = dict()
		for node in nodes_status:
			if node['element_type'] == 'neuron' or node['element_type'] == 'simulator':
				# print node['global_id'] , 'connect with' , self.spike_detectors[node['global_id']]
				nest.Connect(node['global_id'] , self.spike_detectors[node['global_id']] )
				self.spike_dict[self.spike_detectors[node['global_id']]] = node['global_id']

	###########
	# Function:
	#   create spike detectors and connect with all neurons and spike generators
	# Parameter:
	#   log_file : the name of the output file
    #   log_dir  : the name of the output directory
	###########
	def CatchTrace(self,log_file='',log_dir=''):

		print '======== Trace Begin ========'
		# make a director for the logs
		if log_file=='':
			log_file = self.log_file
		if not(log_dir == ''):
			if not(os.path.isdir(log_dir)):
				os.mkdir(log_dir)
			log_file = log_dir+'/'+log_file

		# print all the information
		data = nest.GetStatus(self.spike_detectors)
		__console__ = sys.stdout

		fout = open(log_file+'_spike.csv','w')
		sys.stdout = fout
		# for each  spike_detector
		for i in range(len(data)):
			if not(self.spike_detectors[i] in self.spike_dict.keys() ):
				continue
			# sys.stdout = __console__
			# print self.spike_detectors[i] , 'connect_with' , self.spike_dict[self.spike_detectors[i]]
			# print self.log_file+'/'+str(self.spike_dict[self.spike_detectors[i]])+'.csv'	

			events = data[i]['events']
			# print events
			ne = len(events['times'])
			# fout = open(self.log_file+'/'+str(self.spike_dict[self.spike_detectors[i]])+'.csv', 'w')
			# sys.stdout = fout
			# for each events
			for j in range(ne):
				print str(events['senders'][j]) + SEPERATOR_WORD + str(events['times'][j]) + SEPERATOR_LINE

		fout.close()

		sys.stdout = __console__

		print '======== Trace End ========'

	def __init__(self,log_file='log',if_init=True):
		if if_init:
			self.Init()
		self.log_file = log_file