import nest
import numpy as np 
from NeuroTools import signals

#Initialization
nest.ResetKernel()

nest.SetKernelStatus({"resolution": .01 })

nest.SetKernelStatus({"overwrite_files": True})

#Create a proputation
hh_neuron = nest.Create("hh_cond_exp_traub", n = 20 )

for k in range(20):
	nest.SetStatus([hh_neuron[k]] , {"I_e": k*100.})

sd = nest.Create('spike_detector')

nest.SetStatus(sd , {'to_file': True })

#Connect to spike detector
nest.Connect(hh_neuron , sd)

sd_fileName = 'spike_detector-' + str(sd[0]) + '-0.gdf'

data_file = signals.NestFile(sd_fileName , with_time = True)

spikes = signals.load_spikelist(data_file, dims = 1, id_list= list(hh_neuron) )

# help spikes.raster_plot

# nest.Connect(voltmeter , hh_neuron)

# nest.Simulate(200.)

# vm = np.loadtxt('voltmeter-2-0.dat')

# plot(vm[:,1] , vm[:,2])

print '=======finish======='

