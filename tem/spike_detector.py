import nest
import numpy as np
import pylab as pl

#init
nest.ResetKernel()
nest.SetKernelStatus({"resolution": .01 })


#Create the neuron network
n = 2
neuronsA = nest.Create("iaf_cond_exp", n )
neuronsB = nest.Create("iaf_cond_exp", n )

# nest.CopyModel("static_synapse","excitatory",{"weight":2.5,"delay":0.5})
# nest.Connect( neuronsA , neuronsB , syn_spec="excitatory")

# syn_dict = {'model': 'stdp_synapse',
# 			'weight':2.5,
# 			'delay':{'distribution':'uniform','low':0.8,'high':2.5},
# 			'alpha':{'distribution':'normal_clipped','low':.5,'mu':5.0,'sigma':1.0}}
# nest.Connect( neuronsA , neuronsB   , syn_spec = syn_dict )

#Create the spike generator
print '=====spike generator======='

gex = nest.Create('spike_generator', n , params={'spike_times':np.array([10.0,10.1,10.2,20.0,50.0])})
gin = nest.Create('spike_generator', n ,params={'spike_times':np.array([15.0,25.0,55.0])})


# nest.Connect(gex,neuronsA,params={'weight': 40.0})
# nest.Connect(gin,neuronsA,params={'weight':-20.0})

for i in range(n):
	nest.Connect(gex[i],neuronsA[i], .0,.5)
	nest.Connect(gin[i],neuronsA[i],-20.0,.5)

# Create spike detector
print '======spike detector========'
sd = nest.Create('spike_detector',n)
nest.Connect(neuronsA,sd,'one_to_one')

voltmeter = nest.Create('multimeter', n , params={'record_from': ['V_m']})
nest.SetStatus(voltmeter,{"withtime": True})
nest.Connect(voltmeter,neuronsA)

#Simulate
nest.Simulate(1000.0)

#Check connection
connections = nest.GetConnections()
print '====print the connection info======='
for i in range(len(connections)):
	print '[Connection' , i , '] ' , nest.GetStatus([connections[i]])

# get result
data = nest.GetStatus(sd)

print '=====data======'
print data

mcolor = ['k','b','y','g','c','m']
for i in xrange(len(sd)):
	a,b = data[i]['events']['times'],data[i]['events']['senders']
	print 'data[',i, '] a ' ,a ,' ; b ' ,b
	# pl.subplot(212)
	# pl.scatter(a,b,marker='.', color = mcolor[i%6])

# pl.subplot(212)
# pl.ylabel('Rate(Hz)')
# pl.xlabel('Time')
# pl.hist(a,20)

voltmeter_data = nest.GetStatus(voltmeter)
pl.subplot(211)
pl.plot(voltmeter_data[0]['events']['times'], \
		voltmeter_data[0]['events']['V_m'])


pl.show() 




